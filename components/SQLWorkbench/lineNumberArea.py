from PyQt5.Qt import *

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.edit = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.edit.lineNumberAreaPaintEvent(event)
