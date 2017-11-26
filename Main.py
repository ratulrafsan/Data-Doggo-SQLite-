import sys

from PyQt5.Qt import *

from components.SQLWorkbench.SQLWorkbench import SQLWorkbench
from loadDatabase import Loader


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mainSection = Loader()
        self.sqlWorkstation = SQLWorkbench()
        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.mainSection)
        self.setLayout(self.vbox)

        self.dockwidget = QDockWidget("Execute SQL")
        self.dockwidget.resize(500, 350)
        self.dockwidget.setWidget(self.sqlWorkstation)
        self.dockwidget.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dockwidget)
        self.setCentralWidget(self.mainSection)

        self.statusBar().showMessage("ready")
        self.setWindowTitle("Data Doggo")
        self.setGeometry(300, 300, 600, 400)
        self.show()


app = QApplication(sys.argv)
ex = Main()
sys.exit(app.exec_())