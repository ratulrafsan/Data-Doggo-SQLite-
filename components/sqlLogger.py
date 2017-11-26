from PyQt5.Qt import *

class Logger(QWidget):
    def __init__(self):
        super().__init__()

        self.userCode = []
        self.totalUserCode = 0

    def addUserCode(self, code):
        self.userCode.append(code)
        self.totalUserCode += 1
