from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QGridLayout, QWidget, QComboBox
from PyQt6.QtCore import Qt
import sqlite3
import sys
import re
from PyQt6.QtGui import QIcon
app = QApplication(sys.argv)

# to define a user, we had to define a class


class User:
    def __init__(self):
        self.firstName = None
        self.lastName = None
        self.nationalId = None
        self.phoneNumber = None
        self.userName = None
        self.password = None
        self.city = None
        self.email = None
        self.birthDate = None
        self.securityQAnswer = None
    # بررسی معتبر بودن اسم کوچک و تعریف آن برای کاربر

    def get_first_name(self, firstName):
        if len(re.findall('[a-z]', firstName))+len(re.findall('[A-Z]', firstName)) == len(firstName):
            self.firstName = firstName
        else:
            raise ValueError(
                'first name must only consist of English letters.')
    # بررسی معتبر بودن نام خانوادگی و تعریف آن برای کاربر

    def get_last_name(self, lastName):
        if len(re.findall('[a-z]', lastName))+len(re.findall('[A-Z]', lastName)) == len(lastName):
            self.lastName = lastName
        else:
            raise ValueError('last name must only consist of English letters.')
    # بررسی معتبر بودن کد ملی و تعریف آن برای کاربر

    def get_code_meli(self, nationalId):
        if len(nationalId) == 10:
            if len(re.findall('[0-9]', nationalId)) == len(nationalId):
                self.nationalId = nationalId
            else:
                raise ValueError('National ID only has numbers in it.')
        else:
            raise ValueError('National ID must have ten numbers.')
    # بررسی معتبر بودن شماره تلفن و تعریف آن برای کاربر

    def get_phone_number(self, phoneNumber):
        if len(phoneNumber) == 11 and len(re.findall('[0-9]', phoneNumber)) == len(phoneNumber) and bool(re.search('^09.', phoneNumber)) == True:
            self.phoneNumber = phoneNumber
        elif len(phoneNumber) != 11:
            raise ValueError('phone number must have eleven digits.')
        elif len(re.findall('[0-9]', phoneNumber)) != len(phoneNumber):
            raise ValueError('phone number must only consist of digits.')
        elif bool(re.search('^09.', phoneNumber)) == False:
            raise ValueError('[red]phone number must begin with 09.')
    # گرفتن یوزرنیم از کاربر  که می تواند به هر شکل دلخواه باشد.

    def get_username(self, userName, database):
        database.cursor.execute(
            "SELECT user_name FROM users WHERE user_name=?", (userName,))
        result = database.cursor.fetchone()
        if result:
            raise ValueError("This user name already exists")
        else:
            self.userName = userName
    # گرفتن پسورد در صورتی که شرایط دلخواه مسئله را رعایت کند

    def get_password(self, password):
        if len(password) >= 6 and len(re.findall('[a-z]', password)) >= 1 and len(re.findall('[A-Z]', password)) >= 1 and len(re.findall("[!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]", password)) >= 1 and len(re.findall('[0-9]', password)) >= 1:
            self.password = password
        elif len(password) < 6:
            raise ValueError('password must be at least 6 characters long.')
        elif len(re.findall('[a-z]', password)) < 1:
            raise ValueError(
                'password must contain at least one lowercase letter.')
        elif len(re.findall('[A-Z]', password)) < 1:
            raise ValueError(
                'password must contain at least one uppercase letter.')
        elif len(re.findall("!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"), password) < 1:
            raise ValueError('password must contain at least one digit.')
        elif len(re.findall('[0-9]', password)) < 1:
            raise ValueError(
                'password must contain at least one special character (!#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~).')
    # برای تایید رمز عبور

    def check_repeated_password(self, repeatedPassword):
        if repeatedPassword != self.password:
            raise ValueError('passwords do not match')
        else:
            return 0
    # گرفتن نام شهر از کاربر از لیست شهر های تعریف شده در رابط گرافیکی

    def get_city(self, city):
        self.city = city
    # بررسی معتبر بودن ایمیل و گرفتن از کاربر

    def get_email(self, email, database):
        database.cursor.execute(
            "SELECT email FROM users WHERE email=?", (email,))
        result = database.cursor.fetchone()
        if result:
            raise ValueError("This email already exists")
        else:
            if bool(re.findall(r'[A-Za-z0-9]+@(gmail|yahoo)\.com', email)) == True:
                self.email = email
            else:
                raise ValueError('Invalid email')

    def get_birth_date(self, birthDate):
        if bool(re.findall('[1-2][0-9][0-9][0-9]/[0-1][0-9]/[0-3][0-9]', birthDate)) == True:
            year = birthDate[0:4]
            month = birthDate[5:7]
            day = birthDate[8:10]
            if int(year) >= 1920 and int(year) <= 2005 and 1 <= int(month) <= 12:
                max_days = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31,
                            6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
                if 1 <= int(day) <= max_days[int(month)]:
                    self.birthDate = birthDate
                else:
                    raise ValueError(f'invalid day. this month has only {max_days[int(month)]}')
            elif int(year) < 1920 or int(year) > 2005:
                raise ValueError(f'birth year must be between 1920 and 2005')
            elif int(month) < 1 or int(month) > 12:
                raise ValueError(f'month must be between 1 and 12')
        else:
            raise ValueError(f'invalid birth date format')
    # گرفتن پاسخ سوال امنیتی که از کاربر پرسیده می شود

    def get_security_questions_answer(self, answer):
        self.securityQAnswer = answer
    # اطلاعات کاربر در یک دیتابیس ذخیره می شود

    def save_database(self, database):
        database.cursor.execute("INSERT INTO users(first_name, last_name, national_id, phone_number, user_name, password, city, email, birth_date, security_q_answer) VALUES(?,?,?,?,?,?,?,?,?,?)",
                                (self.firstName, self.lastName, self.nationalId, self.phoneNumber, self.userName, self.password, self.city, self.email, self.birthDate, self.securityQAnswer))
        database.commit()

class Category:
    def __init__(self, name):
        self.name = name

    def validate_name(self):
        if not self.name:
            raise ValueError("Category name cannot be empty")
        if len(self.name) > 15:
            raise ValueError("Category name cannot be longer than 15 characters")
        if not re.match("^[A-Za-z0-9]*$", self.name):
            raise ValueError("Category name can only contain English letters and numbers")

    def save_to_database(self, db, category_type):
        cursor = db.cursor
        cursor.execute(f"SELECT name FROM {category_type} WHERE name=?", (self.name,))
        if cursor.fetchone():
            raise ValueError("Category name already exists")
        cursor.execute(f"INSERT INTO {category_type} (name) VALUES (?)", (self.name,))
        db.commit()
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("QtVersion/Logo.png"))
        self.setWindowTitle("ElmosBalance")
        self.setFixedSize(800, 600)
        self.showMaximized()
        self.db = DataBase()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.signupLoginMenu = SignupLoginMenu(self)


class DataBase:
    def __init__(self):
        self.db = sqlite3.connect("ElmosBalance.db")
        self.cursor = self.db.cursor()
        self.create_data_base()

    def commit(self):
        self.db.commit()

    def create_data_base(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (first_name TEXT, last_name TEXT, national_id TEXT, phone_number TEXT, user_name TEXT PRIMARY KEY, password TEXT, city TEXT, email TEXT, birth_date TEXT, security_q_answer TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS income_categories (name TEXT PRIMARY KEY)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS expense_categories (name TEXT PRIMARY KEY)")

class SignupLoginMenu():
    def __init__(self, window: MyWindow):
        self.window = window
        self.singuping=False
        self.logining=False
        self.login_signup_menu()

    def login_signup_menu(self):
        self.welcominglabel = QLabel(
            'Welcome to elmos balance. If you wish to continue, press login or signup.', self.window)
        self.welcominglabel.setGeometry(150, 100, 400, 200)
        self.welcominglabel.show()
        self.signupButton = QPushButton('Sign up', self.window)
        self.signupButton.setGeometry(300, 250, 200, 50)
        self.signupButton.clicked.connect(self.signup)
        self.signupButton.show()
        self.signinButton = QPushButton('Log in', self.window)
        self.signinButton.setGeometry(300, 350, 200, 50)
        self.signinButton.clicked.connect(self.login)
    # functions for signup
        self.signinButton.show()

    def signup(self):
        # hiding buttons and the label from the very beginning menu
        self.welcominglabel.hide()
        self.signupButton.hide()
        self.signinButton.hide()
        self.user = User()
        self.layout = QGridLayout(self.window.centralWidget())
        # variables for first name
        self.firstNameLabel = QLabel('enter your first name: ', self.window)
        self.firstNameLine = QLineEdit(self.window)
        self.firstnamewarning = QLabel(' ', self.window)
        # variables for last name
        self.lastNameLabel = QLabel('enter your last name: ', self.window)
        self.lastNameLine = QLineEdit(self.window)
        self.lastnamewarning = QLabel(' ', self.window)
        # variables for national id
        self.nationalIDLabel = QLabel('enter your national id: ', self.window)
        self.nationalIDLine = QLineEdit(self.window)
        self.nationalIDwarning = QLabel(' ', self.window)
        # variables for phone number
        self.phoneNumberLabel = QLabel(
            'enter your phone number: ', self.window)
        self.phoneNumberLine = QLineEdit(self.window)
        self.phonenumberwarning = QLabel(' ', self.window)
        # variabled for user name
        self.userNameLabel = QLabel('enter your user name: ', self.window)
        self.userNameLine = QLineEdit(self.window)
        self.usernamewarning = QLabel(' ', self.window)
        # variables for password
        self.passwordLabel = QLabel('enter your password: ', self.window)
        self.passwordLine = QLineEdit(self.window)
        self.passwordLine.setEchoMode(QLineEdit.EchoMode.Password)
        self.passwordwarning = QLabel(' ', self.window)
        # variables for repeated password
        self.repeatedpasswordLabel = QLabel(
            'confirm your password: ', self.window)
        self.repeatedpasswordLine = QLineEdit(self.window)
        self.repeatedpasswordLine.setEchoMode(QLineEdit.EchoMode.Password)
        self.repeatedpasswordwarning = QLabel(' ', self.window)
        # variables for choosing the city
        self.cityLabel = QLabel('choose your city: ', self.window)
        self.cityCombobox = QComboBox(self.window)
        self.cities = ['Karaj',
                    'Ardabil',
                    'Bushehr',
                    'Shahrekord',
                    'Tabriz',
                    'Shiraz',
                    'Rasht',
                    'Gorgan',
                    'Hamadan',
                    'Bandar Abas',
                    'Ilam',
                    'Isfahan',
                    'Kerman',
                    'Kermanshah',
                    'Ahwaz',
                    'Yasuj',
                    'Sanandaj',
                    'Khoramabad',
                    'Arak',
                    'Sari',
                    'Bojnurd',
                    'Qazvin',
                    'Qom',
                    'Mashhad',
                    'Semnan',
                    'Zahedan',
                    'Birjand',
                    'Tehran',
                    'Urmia',
                    'Yazd',
                    'Zanjan']
        self.cityCombobox.addItems(self.cities)
        # variables for email
        self.emailLabel = QLabel('enter your email: ', self.window)
        self.emailLine = QLineEdit(self.window)
        self.emailwarning = QLabel(' ', self.window)
        # variables for date
        self.dateLabel = QLabel('enter your birth date: ', self.window)
        self.dateLine = QLineEdit(self.window)
        self.datewarning = QLabel(' ', self.window)
        # variables for security question answers
        self.securityLabel = QLabel('What is your favorite car brand?')
        self.securityLine = QLineEdit(self.window)
        # submit button
        self.submit = QPushButton('Submit', self.window)
        self.submit.clicked.connect(self.submit_button)
        # show and set layout
        self.layout.addWidget(self.firstNameLabel, 0, 0)
        self.layout.addWidget(self.firstNameLine, 0, 1)
        self.layout.addWidget(self.firstnamewarning, 0, 2)
        self.layout.addWidget(self.lastNameLabel, 1, 0)
        self.layout.addWidget(self.lastNameLine, 1, 1)
        self.layout.addWidget(self.lastnamewarning, 1, 2)
        self.layout.addWidget(self.nationalIDLabel, 2, 0)
        self.layout.addWidget(self.nationalIDLine, 2, 1)
        self.layout.addWidget(self.nationalIDwarning, 2, 2)
        self.layout.addWidget(self.phoneNumberLabel, 3, 0)
        self.layout.addWidget(self.phoneNumberLine, 3, 1)
        self.layout.addWidget(self.phonenumberwarning, 3, 2)
        self.layout.addWidget(self.userNameLabel, 4, 0)
        self.layout.addWidget(self.userNameLine, 4, 1)
        self.layout.addWidget(self.usernamewarning, 4, 2)
        self.layout.addWidget(self.passwordLabel, 5, 0)
        self.layout.addWidget(self.passwordLine, 5, 1)
        self.layout.addWidget(self.passwordwarning, 5, 2)
        self.layout.addWidget(self.repeatedpasswordLabel, 6, 0)
        self.layout.addWidget(self.repeatedpasswordLine, 6, 1)
        self.layout.addWidget(self.repeatedpasswordwarning, 6, 2)
        self.layout.addWidget(self.cityLabel, 7, 0)
        self.layout.addWidget(self.cityCombobox, 7, 1)
        self.layout.addWidget(self.emailLabel, 8, 0)
        self.layout.addWidget(self.emailLine, 8, 1)
        self.layout.addWidget(self.emailwarning, 8, 2)
        self.layout.addWidget(self.dateLabel, 9, 0)
        self.layout.addWidget(self.dateLine, 9, 1)
        self.layout.addWidget(self.datewarning, 9, 2)
        self.layout.addWidget(self.securityLabel, 10, 0)
        self.layout.addWidget(self.securityLine, 10, 1)
        self.layout.addWidget(self.submit, 11, 0, 1, 3)

    def get_first_name(self):
        try:
            self.firstNameLineText = self.firstNameLine.text()
            self.user.get_first_name(self.firstNameLineText)
            if self.firstnamewarning.text() != ' ':
                self.firstnamewarning.setText(' ')
        except ValueError as e:
            error = str(e)
            self.firstnamewarning.setText(error)

    def get_last_name(self):
        try:
            self.lastNameLineText = self.lastNameLine.text()
            self.user.get_last_name(self.lastNameLineText)
            if self.lastnamewarning.text() != ' ':
                self.lastnamewarning.setText(' ')
        except ValueError as e:
            error = str(e)
            self.lastnamewarning.setText(error)

    def get_code_meli(self):
        try:
            self.nationalIDLineText = self.nationalIDLine.text()
            self.user.get_code_meli(self.nationalIDLineText)
            if self.nationalIDwarning.text() != ' ':
                self.nationalIDwarning.setText(' ')
        except ValueError as e:
            error = str(e)
            self.nationalIDwarning.setText(error)

    def get_phone_number(self):
        try:
            self.phoneNumberLineText = self.phoneNumberLine.text()
            self.user.get_phone_number(self.phoneNumberLineText)
            if self.phonenumberwarning.text() != ' ':
                self.phonenumberwarning.setText(' ')
        except ValueError as e:
            error = str(e)
            self.phonenumberwarning.setText(error)

    def get_user_name(self):
        try:
            self.userNameLineText = self.userNameLine.text()
            self.user.get_username(self.userNameLineText, self.window.db)
            if self.usernamewarning.text != ' ':
                self.usernamewarning.setText(' ')
        except ValueError as e:
            error = str(e)
            self.usernamewarning.setText(error)

    def get_password(self):
        try:
            self.passwordLineText = self.passwordLine.text()
            self.user.get_password(self.passwordLineText)
            if self.passwordwarning.text != ' ':
                self.passwordwarning.setText(' ')
        except ValueError as e:
            error = str(e)
            self.passwordwarning.setText(error)

    def check_repeated_password(self):
        try:
            self.repeatedpasswordLineText = self.repeatedpasswordLine.text()
            passwordIsSet = self.user.check_repeated_password(
                self.repeatedpasswordLineText)
            if self.repeatedpasswordwarning.text != ' ':
                self.repeatedpasswordwarning.setText(' ')
        except ValueError as e:
            error = str(e)
            self.repeatedpasswordwarning.setText(error)

    def get_city(self):
        self.user.get_city(self.cityCombobox.currentText())

    def get_email(self):
        try:
            self.emailLineText = self.emailLine.text()
            self.user.get_email(self.emailLineText, self.window.db)
            if self.emailwarning.text != ' ':
                self.emailwarning.setText(' ')
        except ValueError as e:
            error = str(e)
            self.emailwarning.setText(error)

    def get_birth_date(self):
        try:
            self.dateLineText = str(self.dateLine.text())
            self.user.get_birth_date(self.dateLineText)
            if self.datewarning.text != ' ':
                self.datewarning.setText(' ')
        except ValueError as e:
            error = str(e)
            self.datewarning.setText(error)

    def get_security_questions_answer(self):
        self.securityLineText = self.securityLine.text()
        self.user.get_security_questions_answer(self.securityLineText)

    def clear_layout(self, layout):
        for row in range(layout.rowCount()):
            for column in range(layout.columnCount()):
                item = layout.itemAtPosition(row, column)
                if item:
                    widget = item.widget()
                    if widget:
                        widget.setVisible(False)

    def return_layout(self, layout):
        for row in range(layout.rowCount()):
            for column in range(layout.columnCount()):
                item = layout.itemAtPosition(row, column)
                if item:
                    widget = item.widget()
                    if widget:
                        widget.setVisible(False)

    def submit_button(self):
        self.valid = True
        self.get_first_name()
        self.get_last_name()
        self.get_code_meli()
        self.get_phone_number()
        self.get_user_name()
        self.get_password()
        self.check_repeated_password()
        self.get_city()
        self.get_email()
        self.get_birth_date()
        self.get_security_questions_answer()
        if self.firstnamewarning.text() != ' ' or self.lastnamewarning.text() != ' ' or self.nationalIDwarning.text() != ' ' or self.phonenumberwarning.text() != ' ' or self.usernamewarning.text() != ' ' or self.passwordwarning.text() != ' ' or self.repeatedpasswordwarning.text() != ' ' or self.emailwarning.text() != ' ' or self.datewarning.text() != ' ':
            self.valid = False
        if self.valid:
            self.singuping=True
            self.user.save_database(self.window.db)
            self.clear_layout(self.layout)
            self.mainMenu = MainMenu(self.window)
    # functions for login

    def login(self):
        self.welcominglabel.hide()
        self.signupButton.hide()
        self.signinButton.hide()
        # variables for user name
        self.loginlayout = QGridLayout(self.window.centralWidget())
        self.userNameLoginLabel = QLabel('enter your username: ', self.window)
        self.userNameLoginLine = QLineEdit(self.window)
        # variables for password
        self.passwordLoginLabel = QLabel('enter your password: ', self.window)
        self.passwordLoginLine = QLineEdit(self.window)
        self.passwordLoginLine.setEchoMode(QLineEdit.EchoMode.Password)
        # submit button
        self.Loginsubmit = QPushButton('Submit', self.window)
        self.Loginsubmit.clicked.connect(self.submit_login)
        # warning if the username or password was wrong
        self.Loginwarning = QLabel(' ', self.window)
        # variables for forget password
        self.forgetpassword = QLabel('forgot password', self.window)
        self.forgetpassword.mousePressEvent = self.forget_password
        # layout
        self.loginlayout.addWidget(self.userNameLoginLabel, 0, 0)
        self.loginlayout.addWidget(self.userNameLoginLine, 0, 1)
        self.loginlayout.addWidget(self.passwordLoginLabel, 1, 0, 1, 1)
        self.loginlayout.addWidget(self.passwordLoginLine, 1, 1, 1, 1)
        self.loginlayout.addWidget(self.Loginwarning, 3, 1, 1, 1)
        self.loginlayout.addWidget(self.Loginsubmit, 2, 1)
        self.loginlayout.addWidget(self.forgetpassword, 2, 0)
        self.loginlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def check_user_and_pass(self):
        self.window.db.cursor.execute("SELECT user_name,password FROM users WHERE user_name=? AND password=?", (
            self.userNameLoginLine.text(), self.passwordLoginLine.text()))
        result = self.window.db.cursor.fetchone()
        if result:
            self.logining=True
            self.clear_layout(self.loginlayout)
            self.mainMenu = MainMenu(self.window)
        else:
            self.Loginwarning.setText('username or password is wrong')

    def submit_login(self):
        self.check_user_and_pass()

    def forget_password(self, event):
        self.clear_layout(self.loginlayout)
        self.userEmailLabel = QLabel(
            'Enter your username or email:', self.window)
        self.userEmailLine = QLineEdit(self.window)
        self.forgetwarning = QLabel(' ', self.window)
        self.forgetsubmit = QPushButton('Submit', self.window)
        self.forgetsubmit.clicked.connect(self.check_data)
        self.loginlayout.addWidget(self.userEmailLabel, 0, 0)
        self.loginlayout.addWidget(self.userEmailLine, 0, 1)
        self.loginlayout.addWidget(self.forgetsubmit, 1, 1, 1, 1)
        self.loginlayout.addWidget(self.forgetwarning, 2, 1, 1, 1)

    def check_data(self):
        self.window.db.cursor.execute("SELECT user_name,email FROM users WHERE user_name=? OR email=?", (
            self.userEmailLine.text(), self.userEmailLine.text()))
        result = self.window.db.cursor.fetchone()
        if result:
            self.forgetwarning.setText(' ')
            self.forgetsubmit.clicked.disconnect()
            self.questionLabel = QLabel(
                'What is your favorite Car Brand? ', self.window)
            self.questionLine = QLineEdit(self.window)
            self.userEmailLabel.setVisible(False)
            self.userEmailLine.setVisible(False)
            self.forgetsubmit.setVisible(False)
            self.loginlayout.addWidget(self.questionLabel, 0, 0)
            self.loginlayout.addWidget(self.questionLine, 0, 1)
            self.forgetsubmit = QPushButton('Submit', self.window)
            self.forgetsubmit.clicked.connect(self.check_security)
            self.loginlayout.addWidget(self.forgetsubmit, 1, 1)
        else:
            self.forgetwarning.setText('this username/email does not exist')

    def check_security(self):
        self.window.db.cursor.execute(
            "SELECT security_q_answer FROM users WHERE security_q_answer=? ", (self.questionLine.text(),))
        answer = self.window.db.cursor.fetchone()
        if answer:
            self.window.db.cursor.execute("SELECT password FROM users WHERE user_name=? OR email=?", (
                self.userEmailLine.text(), self.userEmailLine.text()))
            password = self.window.db.cursor.fetchone()
            self.forgetwarning.setText(f'your password is: {password[0]}')
        else:
            self.forgetwarning.setText('your security answer was wrong.')

class CategoryMenu:
    def __init__(self, window: MyWindow):
        self.window = window
        self.init_ui()

    def init_ui(self):
        self.window.signupLoginMenu.mainMenu.hide_menu()
        central_widget = QWidget(self.window)
        self.window.setCentralWidget(central_widget)
        self.layout = QGridLayout(central_widget)
        
        self.categoryTypeLabel = QLabel('Select category type: ', self.window)
        self.categoryTypeComboBox = QComboBox(self.window)
        self.categoryTypeComboBox.addItems(['Income', 'Expense'])
        
        self.categoryNameLabel = QLabel('Enter category name: ', self.window)
        self.categoryNameLineEdit = QLineEdit(self.window)
        self.categoryNameWarning = QLabel(' ', self.window)
        
        self.submitButton = QPushButton('Submit', self.window)
        self.submitButton.clicked.connect(self.submit_category)
        
        self.layout.addWidget(self.categoryTypeLabel, 0, 0)
        self.layout.addWidget(self.categoryTypeComboBox, 0, 1)
        self.layout.addWidget(self.categoryNameLabel, 1, 0)
        self.layout.addWidget(self.categoryNameLineEdit, 1, 1)
        self.layout.addWidget(self.categoryNameWarning, 1, 2)
        self.layout.addWidget(self.submitButton, 2, 0, 1, 3)

    def submit_category(self):
        category_type = self.categoryTypeComboBox.currentText().lower() + '_categories'
        category_name = self.categoryNameLineEdit.text()
        category = Category(category_name)
        
        try:
            category.validate_name()
            category.save_to_database(self.window.db, category_type)
            self.categoryNameWarning.setText('Category added successfully')
        except ValueError as e:
            self.categoryNameWarning.setText(str(e))
class MainMenu():
    def __init__(self, window:MyWindow):
        self.window = window
        self.show_main_menu()
    def register_income(self):
        # Implement action for Register Income button
        pass

    def register_expense(self):
        # Implement action for Register Expense button
        pass

    def show_categories(self):
        self.categoryMenu=CategoryMenu(self.window)
        pass

    def show_search(self):
        # Implement action for Search button
        pass

    def show_reporting(self):
        # Implement action for Reporting button
        pass

    def show_settings(self):
        # Implement action for Settings button
        pass
    def show_main_menu(self):
        # Welcome label
        self.welcominglabel = QLabel('Welcome to elmos balance.', self.window)
        self.welcominglabel.setGeometry(150, 100, 400, 200)
        self.welcominglabel.show()

        # Register Income button
        self.registerIncomeButton = QPushButton('Register Income', self.window)
        self.registerIncomeButton.setGeometry(100, 250, 200, 50)
        self.registerIncomeButton.clicked.connect(self.register_income)
        self.registerIncomeButton.show()

        # Register Expense button
        self.registerExpenseButton = QPushButton(
            'Register Expense', self.window)
        self.registerExpenseButton.setGeometry(350, 250, 200, 50)
        self.registerExpenseButton.clicked.connect(self.register_expense)
        self.registerExpenseButton.show()

        # Categories button
        self.categoriesButton = QPushButton('Categories', self.window)
        self.categoriesButton.setGeometry(100, 350, 200, 50)
        self.categoriesButton.clicked.connect(self.show_categories)
        self.categoriesButton.show()

        # Search button
        self.searchButton = QPushButton('Search', self.window)
        self.searchButton.setGeometry(350, 350, 200, 50)
        self.searchButton.clicked.connect(self.show_search)
        self.searchButton.show()

        # Reporting button
        self.reportingButton = QPushButton('Reporting', self.window)
        self.reportingButton.setGeometry(100, 450, 200, 50)
        self.reportingButton.clicked.connect(self.show_reporting)
        self.reportingButton.show()

        # Settings button
        self.settingsButton = QPushButton('Settings', self.window)
        self.settingsButton.setGeometry(350, 450, 200, 50)
        self.settingsButton.clicked.connect(self.show_settings)
        self.settingsButton.show()

        # Exit button
        self.exitButton = QPushButton('Exit', self.window)
        self.exitButton.setGeometry(250, 550, 200, 50)
        self.exitButton.clicked.connect(self.exit_app)
        self.exitButton.show()
    def exit_app(self):
        # Implement action for Exit button
        self.window.close()
    def hide_menu(self):
        self.welcominglabel.setVisible(False)
        self.registerIncomeButton.setVisible(False)
        self.registerExpenseButton.setVisible(False)
        self.categoriesButton.setVisible(False)
        self.searchButton.setVisible(False)
        self.reportingButton.setVisible(False)
        self.settingsButton.setVisible(False)
        self.exitButton.setVisible(False)




if __name__ == '__main__':
    window = MyWindow()
    window.show()
    sys.exit(app.exec())