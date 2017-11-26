from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class SQLWorkbench(QWidget):
    def __init__(self):
        super().__init__()

        self.parentLayout = QVBoxLayout()

        self.x = QLabel("Dock me!")
        self.parentLayout.addWidget(self.x)
        self.initGUI()

    def initGUI(self):
        self.setLayout(self.parentLayout)
