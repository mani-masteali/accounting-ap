from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
from PyQt6.QtGui import QIcon
app = QApplication(sys.argv)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("QtVersion/Logo.png"))
        self.setWindowTitle("ElmosBalance")
        self.showMaximized()


window = MyWindow()
window.show()
sys.exit(app.exec())
