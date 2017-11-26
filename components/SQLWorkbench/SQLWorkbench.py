from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from components.SQLWorkbench.editor import Editor


class SQLWorkbench(QWidget):
    def __init__(self):
        super().__init__()

        self.parentLayout = QVBoxLayout()
        self.toolbarLayout = QHBoxLayout()

        # toolbar
        self.btn_addTab = QToolButton()
        self.btn_saveSql = QToolButton()
        self.btn_runSql = QToolButton()

        # editor tabs
        self.tabCount = 0
        self.editorTabs = QTabWidget()
        self.editorTabList = []

        self.initGUI()

    def initGUI(self):
        self.setupToolbar()
        self.setupEditorTab()
        self.setLayout(self.parentLayout)

    def setupToolbar(self):
        self.btn_addTab.setIcon(QIcon("resources/icon/add_tab.png"))
        self.btn_addTab.setToolTip("Add a new editor tab")
        self.toolbarLayout.addWidget(self.btn_addTab)

        self.btn_runSql.setIcon(QIcon("resources/icon/run.png"))
        self.btn_runSql.setToolTip("Run")
        self.toolbarLayout.addWidget(self.btn_runSql)

        self.btn_saveSql.setIcon(QIcon("resources/icon/save.png"))
        self.btn_saveSql.setToolTip("Save")
        self.toolbarLayout.addWidget(self.btn_saveSql)

        self.btn_addTab.clicked.connect(self.addNewEditorTab)

        self.parentLayout.addLayout(self.toolbarLayout)

    def setupEditorTab(self):
        self.addNewEditorTab()
        self.editorTabs.setTabsClosable(True)
        self.editorTabs.tabCloseRequested.connect(self.removeEditorTab)

        self.parentLayout.addWidget(self.editorTabs)

    def addNewEditorTab(self):
        newEditor = Editor()
        self.editorTabList.append(newEditor)
        self.tabCount += 1
        self.editorTabs.addTab(newEditor, "SQL "+str(len(self.editorTabList)))

    def removeEditorTab(self, index):
        widget = self.editorTabs.widget(index)
        if widget is not None:
            widget.deleteLater()

        for editorReference in self.editorTabList:
            if widget is editorReference:
                self.editorTabList.remove(editorReference)
                break
        self.editorTabs.removeTab(index)
