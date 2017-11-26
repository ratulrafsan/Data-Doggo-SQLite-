import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from structure import DBStructure
from dataBrowser import DataBrowser

from sqlEditor import SQLWorkbench

# Note to experienced qt programmers: I have deliberately ignored QT's sql interface system for this project


class Loader(QWidget):
    def __init__(self):
        super().__init__()

        self.savePath = ""

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
        self.dbStructure = DBStructure()
        self.dataBrowser = DataBrowser()

        self.btn_newDB = QCommandLinkButton(self.label_newDB)
        self.btn_openDB = QCommandLinkButton(self.label_openDB)
        self.btn_writeChanges = QCommandLinkButton(self.label_commitTDB)
        self.btn_rollbackChanges = QCommandLinkButton(self.label_rollbackDB)

        self.initGui()

    def initGui(self):
        self.setupFont()
        self.setupCommandButtons()
        self.setupTabs()
        self.setLayout(self.parentVerticalLayout)

        #self.setWindowTitle("Data Doggo")
        #self.setGeometry(200, 200, 600, 400)
        #self.show()

    def setupCommandButtons(self):
        self.btn_newDB.clicked.connect(self.newDB)
        self.btn_openDB.clicked.connect(self.openDB)
        self.btn_writeChanges.clicked.connect(self.writeChanges)
        self.btn_rollbackChanges.clicked.connect(self.revertChanges)

        self.commandButtonLayout.addWidget(self.btn_newDB)
        self.commandButtonLayout.addWidget(self.btn_openDB)
        self.commandButtonLayout.addWidget(self.btn_writeChanges)
        self.commandButtonLayout.addWidget(self.btn_rollbackChanges)

        self.parentVerticalLayout.addLayout(self.commandButtonLayout)

    def setupTabs(self):
        self.tabs.addTab(self.dbStructure, self.label_dbStructure)
        self.tabs.addTab(self.dataBrowser, self.label_dbBrowser)

        self.parentVerticalLayout.addWidget(self.tabs)

    # create a copy of the original file and operate on the copy until commit
    def openDB(self):
        pass

    # create a new database file via the sqlite database.
    def newDB(self):
        pass

    # commit everything to original file
    def writeChanges(self):
        pass

    # replace original with the backup file
    def revertChanges(self):
        pass

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

    def getFile(self):
        dlg = QFileDialog()
        dlg.setWindowTitle("Open")
        dlg.setViewMode(QFileDialog.Detail)

        if dlg.exec_():
            self.savePath = dlg.selectedFiles()[0]
            self.LE_dbPath.setText(self.savePath)

    def setupFont(self):
        self.font.setFamily("Lucidia")
        self.font.setFixedPitch(True)
        self.font.setPointSize(10)

