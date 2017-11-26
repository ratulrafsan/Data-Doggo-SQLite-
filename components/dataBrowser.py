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

        self.tableView = QTableWidget()
        self.initGUI()

    def initGUI(self):
        self.toolsLayout.addWidget(QLabel("Table: "))
        self.toolsLayout.addWidget(self.tableComboBox)
        self.toolsLayout.addWidget(self.btn_newRecord)
        self.toolsLayout.addWidget(self.btn_deleteRecord)
        self.parentLayout.addLayout(self.toolsLayout)
        self.parentLayout.addWidget(self.tableView)
        self.setLayout(self.parentLayout)

    @pyqtSlot()
    def setupTools(self):

        self.setupComboBox()
        self.btn_newRecord.clicked.connect(self.addNewRow)
        self.btn_deleteRecord.clicked.connect(self.deleteRow)

    def deleteRow(self):
        pass

    def addNewRow(self):
        pass

    def editCell(self):
        pass

    def setupComboBox(self):
        tables = self.loader.dbManager.getListofTables()

        if tables is None:
            if self.loader.dbManager.error != "":
                # TODO: Add proper error message here too!!
                print("Error : " + self.loader.dbManager.error)
                return

        for table in tables:
            self.tableComboBox.addItem(table)

        self.tableComboBox.activated[str].connect(self.setupAndPopulateTable)

        self.defaultTable = tables[0]
        self.setupAndPopulateTable(self.defaultTable)

    def setupAndPopulateTable(self, tableName):
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
            print("Error: " + dbManager.error)
            return

        for dataSet in tableData:
            rowPos = self.tableView.rowCount()
            self.tableView.insertRow(rowPos)
            for i, data in enumerate(dataSet):
                self.tableView.setItem(rowPos, i, QTableWidgetItem(str(data)))