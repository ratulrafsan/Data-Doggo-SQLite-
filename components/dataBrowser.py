from PyQt5.Qt import *

class DataBrowser(QWidget):
    def __init__(self, loader):
        super().__init__()

        self.loader = loader

        self.parentLayout = QVBoxLayout()
        self.toolsLayout = QHBoxLayout()

        self.tableComboBox = QComboBox()
        self.btn_newRecord = QPushButton("New Record")
        self.btn_deleteRecord = QPushButton("Delete Record")

        self.defaultTable = ""
        self.currentTable = ""

        self.prevItemVal = ""
        self.prevRow = None
        self.prevCol = None


        self.tableView = QTableWidget()
        self.initGUI()

    def initGUI(self):
        self.tableView.cellDoubleClicked.connect(self.observe)
        self.toolsLayout.addWidget(QLabel("Table: "))
        self.toolsLayout.addWidget(self.tableComboBox)
        self.toolsLayout.addWidget(self.btn_newRecord)
        self.toolsLayout.addWidget(self.btn_deleteRecord)
        self.parentLayout.addLayout(self.toolsLayout)
        self.parentLayout.addWidget(self.tableView)
        self.setLayout(self.parentLayout)

    @pyqtSlot()
    def setupTools(self):
        self.loader.dbManager.setDataBrowserReference(self)
        self.setupComboBox()
        self.btn_newRecord.clicked.connect(self.addNewRow)
        self.btn_deleteRecord.clicked.connect(self.deleteRow)
        self.loader.dbManager.sqlExecuted.connect(self.updateComboBoxAndViewer)

    def deleteRow(self):
        index = self.tableView.currentIndex()
        column = self.tableView.currentColumn()
        item = self.tableView.itemFromIndex(index)

        columnName = self.loader.dbManager.getColumnNames(self.currentTable)[column]
        self.loader.dbManager.deleteRow(self.currentTable, columnName, item.text())

        self.tableView.model().removeRow(index.row())
        self.tableView.model().submit()


    def addNewRow(self):
        print("adding row")
        self.loader.dbManager.addEmptyRow(self.currentTable)
        self.setupAndPopulateTable(self.currentTable)

    def observe(self, row, col):
        self.prevRow = row
        self.prevCol = col
        print("observing {} {}".format(row, col))
        item = self.tableView.item(row, col)
        self.prevItemVal = item.text()
        self.tableView.itemDelegate().closeEditor.connect(self.checkForChange)

    def checkForChange(self):
        self.tableView.itemDelegate().closeEditor.disconnect(self.checkForChange)
        pItem = self.tableView.item(self.prevRow, self.prevCol)
        print("Checking for changes..")
        if self.prevItemVal == pItem.text():
            print("No change. Continue")
        else:
            print("Change detected. Prev: {} Cur: {}".format(self.prevItemVal, pItem.text()))
            self.doUpdate(pItem.text())

    def doUpdate(self, updatingValue):
        columnList = self.loader.dbManager.getColumnNames(self.currentTable)
        currentRow = self.tableView.currentRow()
        currentCol = self.tableView.currentColumn()
        updatingCol = columnList[currentCol]
        identifierList = list(columnList)
        identifierList.remove(updatingCol)
        identifierDataList = []
        for i in range(0, self.tableView.columnCount()):
            if i != currentCol:
                identifierDataList.append(self.tableView.item(currentRow, i).text())
        self.loader.dbManager.updateQueryConstructor(tableName=self.currentTable,
                                                     identifierList=identifierList,
                                                     identifierDataList=identifierDataList,
                                                     updatingColumn=updatingCol,
                                                     updatingValue=updatingValue)
        self.setupAndPopulateTable(self.currentTable)

    def updateComboBoxAndViewer(self):
        self.tableComboBox.clear()

        tables = self.loader.dbManager.getListofTables()

        if tables == []:
            if self.loader.dbManager.error != "":
                # TODO: Add proper error message here too!!
                print("Error : " + self.loader.dbManager.error)
                return
            return

        for table in tables:
            self.tableComboBox.addItem(table)

        self.setupAndPopulateTable(self.currentTable)

    def setupComboBox(self):
        tables = self.loader.dbManager.getListofTables()

        if tables == []:
            if self.loader.dbManager.error != "":
                # TODO: Add proper error message here too!!
                print("Error : " + self.loader.dbManager.error)
                return
            return

        for table in tables:
            self.tableComboBox.addItem(table)

        self.tableComboBox.activated[str].connect(self.setupAndPopulateTable)

        self.defaultTable = tables[0]
        self.setupAndPopulateTable(self.defaultTable)

    def setupAndPopulateTable(self, tableName):
        self.currentTable = tableName
        while self.tableView.model().rowCount() > 0:
            self.tableView.model().removeRow(0)

        dbManager = self.loader.dbManager
        self.tableView.setColumnCount(dbManager.getColumnCount(tableName))
        #self.tableView.setColumnCount(2)

        columnName = dbManager.getColumnNames(tableName)
        if columnName is None:
            # TODO: Add proper error message
            print("Error: " + dbManager.error)
            return

        self.tableView.setHorizontalHeaderLabels(dbManager.getColumnNames(tableName))

        tableData = dbManager.getAllData(tableName)
        if tableData is None:
            # TODO: Add proper error message
            print("Error: " + str(dbManager.error))
            return

        for dataSet in tableData:
            rowPos = self.tableView.rowCount()
            self.tableView.insertRow(rowPos)
            for i, data in enumerate(dataSet):
                self.tableView.setItem(rowPos, i, QTableWidgetItem(str(data)))

