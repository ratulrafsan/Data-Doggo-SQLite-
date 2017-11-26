from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class DataBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.x = QLabel("hello")
        self.show()