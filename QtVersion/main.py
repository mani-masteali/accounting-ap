from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QGridLayout, QWidget
import sys
import re
from PyQt6.QtGui import QIcon
app = QApplication(sys.argv)

#to define a user, we had to define a class
class User:
    def __init__(self):
        self.firstName=None
        self.lastName=None
        self.nationalId=None
        self.phoneNumber=None
        self.userName=None
        self.password=None
        self.city=None
        self.email=None
        self.birthDate=None
        self.securityQAnswer=None
        self.savedcities = [
            'Alborz',
            'Ardabil',
            'Bushehr',
            'Chaharmahal and Bakhtiari',
            'East Azerbaijan',
            'Fars',
            'Gilan',
            'Golestan',
            'Hamadan',
            'Hormozgan',
            'Ilam',
            'Isfahan',
            'Kerman',
            'Kermanshah',
            'Khuzestan',
            'Kohgiluyeh and Buyer Ahmad',
            'Kurdistan',
            'Lorestan',
            'Markazi',
            'Mazandaran',
            'North Khorasan',
            'Qazvin',
            'Qom',
            'Razavi Khorasan',
            'Semnan',
            'Sistan and Baluchestan',
            'South Khorasan',
            'Tehran',
            'West Azerbaijan',
            'Yazd',
            'Zanjan']            # بررسی معتبر بودن اسم کوچک و تعریف آن برای کاربر
    def get_first_name(self,firstName):
        if len(re.findall('[a-z]',firstName))+len(re.findall('[A-Z]',firstName)) == len(firstName):
            self.firstName=firstName
        else:
            raise ValueError('first name must only consist of English letters.')
    # بررسی معتبر بودن نام خانوادگی و تعریف آن برای کاربر
    def get_last_name(self,lastName):
        if len(re.findall('[a-z]',lastName))+len(re.findall('[A-Z]',lastName)) == len(lastName):
            self.lastName=lastName
        else:
            raise ValueError('last name must only consist of English letters.')
    #بررسی معتبر بودن کد ملی و تعریف آن برای کاربر
    def get_code_meli(self,nationalId):
        if len(nationalId)==10 :
            if len(re.findall('[0-9]',nationalId))==len(nationalId):
                self.nationalId=nationalId
            else:
                raise ValueError('National ID only has numbers in it.')
        else:
            raise ValueError('National ID must have ten numbers.')
    #بررسی معتبر بودن شماره تلفن و تعریف آن برای کاربر
    def get_phone_number(self,phoneNumber):
        if len(phoneNumber)==11 and len(re.findall('[0-9]',phoneNumber))==len(phoneNumber) and  bool(re.search('^09.',phoneNumber))==True:
            self.phoneNumber=phoneNumber
        elif len(phoneNumber)!=11:
            raise ValueError('phone number must have eleven digits.')
        elif len(re.findall('[0-9]',phoneNumber))!=len(phoneNumber):
            raise ValueError('phone number must only consist of digits.')
        elif bool(re.search('^09.',phoneNumber))==False:
            raise ValueError('[red]phone number must begin with 09.')
    #گرفتن یوزرنیم از کاربر  که می تواند به هر شکل دلخواه باشد.
    def get_username(self,userName):
        #will check if the username is not in the database when the database is initialized
        self.userName=userName
    #گرفتن پسورد در صورتی که شرایط دلخواه مسئله را رعایت کند
    def get_password(self,password):
        if len(password)>=6 and len(re.findall('[a-z]',password))>=1 and len(re.findall('[A-Z]',password))>=1 and len(re.findall("[!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]",password))>=1 and len(re.findall('[0-9]',password))>=1:
            self.password=password
        elif len(password)<6:
            raise ValueError('password must be at least 6 characters long.')
        elif len(re.findall('[a-z]',password))<1:
            raise ValueError('password must contain at least one lowercase letter.')
        elif len(re.findall('[A-Z]',password))<1:
            raise ValueError('password must contain at least one uppercase letter.')
        elif len(re.findall("!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"),password)<1:
            raise ValueError('password must contain at least one digit.')
        elif len(re.findall('[0-9]',password))<1:
            raise ValueError('password must contain at least one special character (!#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~).')
    #برای تایید رمز عبور  
    def check_repeated_password(self,repeatedPassword):
        if repeatedPassword!=self.password:
            print('passwords do not match')
    # گرفتن نام شهر از کاربر در صورتی که در لیست تعریف شده باشد
    def get_city(self,city):
        pass
        #will be defined when the city menu is initialized
    # بررسی معتبر بودن ایمیل و گرفتن از کاربر
    def get_email(self,email):
        #will check if the email exists in the database later
        if bool(re.findall(r'[A-Za-z0-9]+@(gmail|yahoo)\.com',email))==True:
            self.email=email
        else:
            raise ValueError('Invalid email')
    def get_birth_date(self,birthDate):
        if bool(re.findall('[1-2][0-9][0-9][0-9]/[0-1][0-9]/[0-3][0-9]',birthDate))==True:
            year=birthDate[0:4]
            month=birthDate[5:7]
            day=birthDate[8:10]
            if int(year)>=1920 and int(year)<=2005 and 1<=int(month)<=12:
                max_days={1:31,2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
                if 1<=int(day)<=max_days[int(month)]:
                    self.birthDate=birthDate
                else:
                    raise ValueError(f'invalid day. this month has only {max_days[month]}')
            elif int(year)<1920 or int(year)>2005:
                raise ValueError(f'birth year must be between 1920 and 2005')
            elif int(month)<1 or int(month)>12:
                raise ValueError(f'month must be between 1 and 12')
        else:
            raise ValueError(f'invalid birth date format')
        return
    #گرفتن پاسخ سوال امنیتی که از کاربر پرسیده می شود
    def get_security_questions_answer(self,answer):
        self.securityQAnswer=answer
    #اطلاعات کاربر در یک دیتابیس ذخیره می شود
    def save_database(self):
        #will be written as soon as the database is ready
        pass

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("QtVersion/Logo.png"))
        self.setWindowTitle("ElmosBalance")
        self.setFixedSize(800,600)
        self.showMaximized()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self._signupmenu=SignupLoginMenu(self)

class SignupLoginMenu():
    def __init__(self,window:MyWindow):
        self.window=window
        self.login_signup_menu()
    def login_signup_menu(self):
        self.welcominglabel=QLabel('Welcome to elmos balance. If you wish to continue, press login or signup.',self.window)
        self.welcominglabel.setGeometry(150,100,400,200)
        self.welcominglabel.show()
        self.signupButton = QPushButton('Sign up',self.window)
        self.signupButton.setGeometry(300,250,200,50)
        self.signupButton.clicked.connect(self.signup)
        self.signupButton.show()
        self.signinButton= QPushButton('Log in',self.window)
        self.signinButton.setGeometry(300,350,200,50)
        self.signinButton.clicked.connect(self.login)
        self.signinButton.show()
    def signup(self):
        #hiding buttons and the label from the very beginning menu
        self.welcominglabel.hide()
        self.signupButton.hide()
        self.signinButton.hide()
        self.user=User()
        layout=QGridLayout(self.window.centralWidget())
        #variables for first name
        self.firstNameLabel=QLabel('enter your first name: ',self.window)
        self.firstNameLine=QLineEdit(self.window)
        self.firstnamewarning=QLabel(' ',self.window)
        #variables for last name
        self.lastNameLabel=QLabel('enter your last name: ',self.window)
        self.lastNameLine=QLineEdit(self.window)
        self.lastnamewarning=QLabel(' ',self.window)
        #variables for national id
        self.nationalIDLabel=QLabel('enter your national id: ',self.window)
        self.nationalIDLine=QLineEdit(self.window)
        self.nationalIDwarning=QLabel(' ',self.window)
        #submit button
        self.submit=QPushButton('Submit',self.window)
        self.submit.clicked.connect(self.submit_button)
        #show and set layout
        layout.addWidget(self.firstNameLabel, 0, 0)
        layout.addWidget(self.firstNameLine, 0, 1)
        layout.addWidget(self.firstnamewarning, 0, 2)
        layout.addWidget(self.lastNameLabel, 1, 0)
        layout.addWidget(self.lastNameLine, 1, 1)
        layout.addWidget(self.lastnamewarning, 1, 2)
        layout.addWidget(self.nationalIDLabel, 2, 0)
        layout.addWidget(self.nationalIDLine, 2, 1)
        layout.addWidget(self.nationalIDwarning, 2, 2)
        layout.addWidget(self.submit, 3, 0, 1, 3)

    def get_first_name(self):
        try:
            self.firstNameLineText=self.firstNameLine.text()
            self.user.get_first_name(self.firstNameLineText)
            print(self.firstNameLineText)
            if self.firstnamewarning.text()!=' ':
                self.firstnamewarning.setText(' ')
        except ValueError as e:
            error=str(e)
            self.firstnamewarning.setText(error)
    def get_last_name(self):
        try:
            self.lastNameLineText=self.lastNameLine.text()
            self.user.get_last_name(self.lastNameLineText)
            print(self.lastNameLineText)
            if self.lastnamewarning.text()!=' ':
                self.lastnamewarning.setText(' ')
        except ValueError as e:
            error=str(e)
            self.lastnamewarning.setText(error)
    def get_code_meli(self):
        try:
            self.nationalIDLineText=self.nationalIDLine.text()
            self.user.get_code_meli(self.nationalIDLineText)
            print(self.nationalIDLineText)
            if self.nationalIDwarning.text()!=' ':
                self.nationalIDwarning.setText(' ')
        except ValueError as e:
            error=str(e)
            self.nationalIDwarning.setText(error)
    def submit_button(self):
        self.get_first_name()
        self.get_last_name()
        self.get_code_meli()
    def login(self):
        self.welcominglabel.hide()
        self.signupButton.hide()
        self.signinButton.hide()

if __name__=='__main__':
    window = MyWindow()
    window.show()
    sys.exit(app.exec())