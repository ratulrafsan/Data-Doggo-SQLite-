from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class DBStructure(QWidget):
    def __init__(self, loader):
        super().__init__()

        # instance of the loader class to fetch the database path and stuff
        self.loader = loader
        self.parentLayout = QVBoxLayout()

        self.treeView = QTreeView()
        self.model = QStandardItemModel()

        self.initGUI()

    # boop
    def initGUI(self):
        self.setLayout(self.parentLayout)

    @pyqtSlot()
    def setupTreeView(self):
        self.loader.dbManager.setdbStrucuteReference(self)
        self.loader.dbManager.sqlExecuted.connect(self.populateTreeView)

        self.populateTreeView()

        self.treeView.setModel(self.model)
        self.treeView.setAlternatingRowColors(True)
        self.parentLayout.addWidget(self.treeView)

    def populateTreeView(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Name", "Type"])
        rootNode = self.model.invisibleRootItem()
        tables = self.loader.dbManager.getListofTables()

        if tables is None:
            if self.loader.dbManager.error != "":
                # TODO: Add proper error message
                print("Error :" + self.loader.dbManager.error)
                return

        tableRootNode = QStandardItem("Tables (" + str(len(tables)) + ")")
        for table in tables:
            colType = self.loader.dbManager.getColumnTypes(table)
            if colType is None:
                if self.loader.dbManager.error != "":
                    # TODO: Add proper error message
                    print("Error : " + self.loader.dbManager.error)
                continue
            # create child table node
            tableNode = QStandardItem(table)
            for dataSet in colType:
                tableNode.appendRow([QStandardItem(dataSet[0]), QStandardItem(dataSet[1])])

            tableRootNode.appendRow([tableNode, None])

        rootNode.appendRow([tableRootNode, None])
