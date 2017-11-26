from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class DBStructure(QWidget):
    def __init__(self):
        super().__init__()
        self.l = QVBoxLayout(self)
        self.setLayout(self.l)
        self.y = QLabel("world")
        self.l.addWidget(self.y)