from shutil import copy2
from os.path import basename, isfile
from os import access, W_OK, R_OK

from PyQt5.Qt import *

from components.dataBrowser import DataBrowser
from components.structure import DBStructure
from components.dbManager import DBManager


# Note to experienced qt programmers: I have deliberately ignored QT's sql interface system for this project


class Loader(QWidget):
    dbLoaded = pyqtSignal()

    def __init__(self, mainWindow):
        super().__init__()

        self.mainWindow = mainWindow

        self.label_newDB = "New Database"
        self.label_openDB = "Open Database"
        self.label_commitTDB = "Write Changes"
        self.label_rollbackDB = "Revert Changes"
        self.label_dbStructure = "Database Structure"
        self.label_dbBrowser = "Data Browser"

        self.font = QFont()

        self.parentVerticalLayout = QVBoxLayout(self)
        self.commandButtonLayout = QHBoxLayout(self)

        self.tabs = QTabWidget()
        self.dbStructure = DBStructure(self)
        self.dataBrowser = DataBrowser(self)
        self.sqlworkbench = None

        self.btn_newDB = QCommandLinkButton(self.label_newDB)
        self.btn_openDB = QCommandLinkButton(self.label_openDB)
        self.btn_writeChanges = QCommandLinkButton(self.label_commitTDB)

        self.databasePath = ""
        self.fileName = ""
        self.tempPath = ""
        self.dbManager = None

        self.written = False
        self.canRevert = True

        self.initGui()

    def initGui(self):
        self.setupFont()
        self.setupCommandButtons()
        self.setupTabs()
        self.setLayout(self.parentVerticalLayout)

        self.dbLoaded.connect(self.dbStructure.setupTreeView)
        self.dbLoaded.connect(self.dataBrowser.setupTools)

    def setupCommandButtons(self):
        self.btn_newDB.clicked.connect(self.newDB)
        self.btn_openDB.clicked.connect(self.newDB)
        self.btn_writeChanges.clicked.connect(self.commitToDB)

        self.commandButtonLayout.addWidget(self.btn_newDB)
        self.commandButtonLayout.addWidget(self.btn_openDB)
        self.commandButtonLayout.addWidget(self.btn_writeChanges)

        self.parentVerticalLayout.addLayout(self.commandButtonLayout)

    def commitToDB(self):
        if self.dbManager is not None:
            self.dbManager.commitToDB()

    def setupTabs(self):
        self.tabs.addTab(self.dbStructure, self.label_dbStructure)
        self.tabs.addTab(self.dataBrowser, self.label_dbBrowser)

        self.parentVerticalLayout.addWidget(self.tabs)

    # create a copy of the original file and operate on the copy until commit(self.writeChanges method)
    def openDB(self):
        filePath = self.chooseFile()
        if filePath is None:
            return


    def newDB(self):
        filePath = self.chooseFile()
        if filePath is None:
            return

        self.dbManager = DBManager(filePath)
        self.dbLoaded.connect(self.sqlworkbench.enableEditor)
        self.databasePath = filePath
        print(self.databasePath)
        if self.databasePath is not None:
            self.dbLoaded.emit()
            self.dbManager.setLoaderReference(self)

    def setupCreateDatabase(self):
        self.LE_dbPath.setFont(self.font)

        self.TE_sqlInput.setFont(self.font)
        self.TE_sqlInput.setMinimumSize(200, 300)

        self.BTN_selectPath.clicked.connect(self.getFile)

        self.pathSectionLayout.addWidget(self.L_dbPath)
        self.pathSectionLayout.addWidget(self.LE_dbPath)
        self.pathSectionLayout.addWidget(self.BTN_selectPath)

        self.createDatabaseLayout.addLayout(self.pathSectionLayout)
        self.createDatabaseLayout.addWidget(self.TE_sqlInput)

        self.parentVerticalLayout.addLayout(self.createDatabaseLayout)

    def chooseFile(self):
        fileChooser = QFileDialog()
        if fileChooser.exec_() == QDialog.Accepted:
            path = fileChooser.selectedFiles()[0]
            if not isfile(path):
                try:
                    f = open(basename(path), 'w')
                except OSError as e:
                    msg = "Cannot create file! " + e
                    QMessageBox.critical(self, "ERROR", msg, QMessageBox.Ok, QMessageBox.Ok)
            # check if the user has r/w permission for the selected file
            if not access(path, W_OK):
                msg = "You do not have {} permission for that file. Continue ?".format(
                    "read-write" if not access(path, R_OK) else "write"
                )
                response = QMessageBox.question(self, 'Notice!', msg,
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if response == QMessageBox.Yes:
                    return path
            return path
        return None

    def setupFont(self):
        self.font.setFamily("Lucidia")
        self.font.setFixedPitch(True)
        self.font.setPointSize(10)


