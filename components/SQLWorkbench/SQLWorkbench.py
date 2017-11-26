from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from components.SQLWorkbench.editor import Editor
from components.sqlLogger import Logger


class SQLWorkbench(QWidget):
    def __init__(self):
        super().__init__()

        self.sqlLogger = Logger()

        self.parentLayout = QVBoxLayout()
        self.toolbarLayout = QHBoxLayout()

        # toolbar
        self.btn_addTab = QToolButton()
        self.btn_saveSql = QToolButton()
        self.btn_runSql = QToolButton()
        self.btn_openSql = QToolButton()

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
        self.btn_addTab.clicked.connect(self.addNewEditorTab)
        self.toolbarLayout.addWidget(self.btn_addTab)

        self.btn_openSql.setIcon(QIcon("resources/icon/open_file.png"))
        self.btn_openSql.setToolTip("Open SQL file")
        self.btn_openSql.clicked.connect(self.openSqlCode)
        self.toolbarLayout.addWidget(self.btn_openSql)

        self.btn_runSql.setIcon(QIcon("resources/icon/run.png"))
        self.btn_runSql.setToolTip("Run")
        self.btn_runSql.clicked.connect(self.getEditorInput)
        self.toolbarLayout.addWidget(self.btn_runSql)

        self.btn_saveSql.setIcon(QIcon("resources/icon/save.png"))
        self.btn_saveSql.setToolTip("Save")
        self.btn_saveSql.clicked.connect(self.saveEditorInput)
        self.toolbarLayout.addWidget(self.btn_saveSql)

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

    def getEditorInput(self):
        editor = self.editorTabs.currentWidget()
        if editor is not None:
            return editor.toPlainText()

    def runEditorInput(self):
        input = self.getEditorInput()
        self.sqlLogger.addUserCode(input)
        # TODO: implement code execution method!

    def openSqlCode(self):
        editor = self.editorTabs.currentWidget()
        filePath = self.chooseFile()
        try:
            with open(filePath, 'r') as f:
                editor.setPlainText(f.read())
        except OSError as e:
            QMessageBox.information(self, "Error!",
                                    "Failed to pen file: " + e,
                                    QMessageBox.Ok, QMessageBox.Ok)


    def chooseFile(self):
        fileChooser = QFileDialog()
        if fileChooser.exec_() == QDialog.Accepted:
            return fileChooser.selectedFiles()[0]


    def saveEditorInput(self):
        filePath = self.chooseFile()
        try:
            with open(filePath, 'w') as f:
                f.write(self.getEditorInput())
        except OSError as e:
            QMessageBox.information(self, "Error!",
                                    "Failed to save file: " + e,
                                    QMessageBox.Ok, QMessageBox.Ok)


