from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MyWindow(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.setWindowTitle(self.tr("simple."))
        self.button = QPushButton(self.tr('button'), self)
        layout = QVBoxLayout()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    translator = QTranslator()
    print translator.load("translate/simple.qm")
    app.installTranslator(translator)
    ui = MyWindow()
    ui.show()
    sys.exit(app.exec_())
