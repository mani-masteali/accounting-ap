from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
import sys
from PyQt6.QtGui import QIcon
app = QApplication(sys.argv)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("QtVersion/Logo.png"))
        self.setWindowTitle("ElmosBalance")
        self.setFixedSize(800,600)
        self.showMaximized()
        self.login_signup_menu()
    def login_signup_menu(self):
        self.welcominglabel=QLabel('Welcome to elmos balance. If you wish to continue, press login or signup.',self)
        self.welcominglabel.setGeometry(150,100,400,200)
        self.welcominglabel.show()
        self.signupButton = QPushButton('Sign up',self)
        self.signupButton.setGeometry(300,250,200,50)
        self.signupButton.clicked.connect(self.signup)
        self.signupButton.show()
        self.signinButton= QPushButton('Log in',self)
        self.signinButton.setGeometry(300,350,200,50)
        self.signinButton.clicked.connect(self.login)
        self.signinButton.show()
    def signup(self):
        self.welcominglabel.hide()
        self.signupButton.hide()
        self.signinButton.hide()
    def login(self):
        self.welcominglabel.hide()
        self.signupButton.hide()
        self.signinButton.hide()

if __name__=='__main__':
    window = MyWindow()
    window.show()
    sys.exit(app.exec())