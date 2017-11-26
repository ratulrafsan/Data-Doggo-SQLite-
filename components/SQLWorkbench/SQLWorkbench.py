from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class SQLWorkbench(QWidget):
    def __init__(self):
        super().__init__()

        self.parentLayout = QVBoxLayout()
        self.toolbarLayout = QHBoxLayout()

        # toolbar
        self.toolbar = QToolBar()
        self.btn_addTab = QToolButton()
        self.btn_saveSql = QToolButton()
        self.btn_runSql = QToolButton()

        self.initGUI()

    def initGUI(self):
        self.setupToolbar()
        self.setLayout(self.parentLayout)

    def setupToolbar(self):
        self.toolbarLayout.addWidget(self.btn_addTab)
        self.toolbarLayout.addWidget(self.btn_runSql)
        self.toolbarLayout.addWidget(self.btn_saveSql)

        self.toolbar.setLayout(self.toolbarLayout)
        self.parentLayout.addWidget(self.toolbar)
        self.parentLayout.addWidget(QLabel("Dock me!"))