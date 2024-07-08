from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QGridLayout, QWidget, QComboBox,QRadioButton,QButtonGroup,QTableView
from PyQt6.QtCore import Qt, QAbstractTableModel,QVariant
from PyQt6.QtGui import QStandardItemModel,QStandardItem
import matplotlib.pyplot as plt
from datetime import datetime
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
                    raise ValueError(f'invalid day. this month has only { max_days[int(month)]}')
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


class RegisterFine:
    def __init__(self, db):
        self.db = db

    def register_income(self, amount, date, category, description,user):
        self.validate_amount(amount)
        self.validate_date(date)
        self.validate_category(category)
        self.validate_description(description)

        cursor = self.db.cursor
        cursor.execute("INSERT INTO income_fine (username, amount, date, category, description) VALUES (?,?,?,?,?)",
                    (user,amount, date, category, description))
        self.db.commit()

    def register_expense(self, amount, date, category, description,user):
        self.validate_amount(amount)
        self.validate_date(date)
        self.validate_category(category)
        self.validate_description(description)

        cursor = self.db.cursor()
        cursor.execute("INSERT INTO expense_fine (username, amount, date, category, description) VALUES (?,?,?,?,?)",
                    (user,amount, date, category, description))
        self.db.commit()

    def validate_amount(self, amount):
        if not amount:
            raise ValueError("Amount cannot be empty")
        if not isinstance(amount, (int, float)):
            raise ValueError("Amount must be a number")
        if amount <= 0:
            raise ValueError("Amount must be positive")

    def validate_date(self, date):
        if not date:
            raise ValueError("Date cannot be empty")
        try:
            datetime.strptime(date, '%Y/%m/%d')
        except ValueError:
            raise ValueError("Invalid date format. Must be yyyy/mm/dd")

    def validate_category(self, category):
        if not category:
            raise ValueError("Category cannot be empty")

    def validate_description(self, description):
        if description and len(description) > 100:
            raise ValueError("Description must be 100 characters or less")

    def create_tables(self):
        cursor = self.db.cursor
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS income_fine (
                username TEXT PRIMARY KEY,
                amount REAL,
                date TEXT,
                category TEXT,
                description TEXT
            )
        """)
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS expense_fine (
                username TEXT PRIMARY KEY,
                amount REAL,
                date TEXT,
                category TEXT,
                description TEXT
            )
        """)
        self.db.commit()

class RegisterIncomeMenu:
    def __init__(self, window: MyWindow):
        self.window = window
        self.init_ui()

    def init_ui(self):
        self.window.signupLoginMenu.mainMenu.hide_menu()
        central_widget = QWidget(self.window)
        self.window.setCentralWidget(central_widget)
        self.layout = QGridLayout(central_widget)

        self.amountLabel = QLabel('Enter amount: ', self.window)
        self.amountLineEdit = QLineEdit(self.window)
        self.amountWarning = QLabel(' ', self.window)

        self.dateLabel = QLabel('Enter date (yyyy/mm/dd): ', self.window)
        self.dateLineEdit = QLineEdit(self.window)
        self.dateWarning = QLabel(' ', self.window)

        self.categoryLabel = QLabel('Select category: ', self.window)
        self.categoryComboBox = QComboBox(self.window)
        self.load_income_categories()

        self.descriptionLabel = QLabel('Enter description: ', self.window)
        self.descriptionLineEdit = QLineEdit(self.window)
        self.descriptionWarning = QLabel(' ', self.window)

        self.submitButton = QPushButton('Submit', self.window)
        self.submitButton.clicked.connect(self.submit_income)
        self.backButton = QPushButton('Back', self.window)
        self.backButton.clicked.connect(self.back)

        self.layout.addWidget(self.amountLabel, 0, 0)
        self.layout.addWidget(self.amountLineEdit, 0, 1)
        self.layout.addWidget(self.amountWarning, 0, 2)
        self.layout.addWidget(self.dateLabel, 1, 0)
        self.layout.addWidget(self.dateLineEdit, 1, 1)
        self.layout.addWidget(self.dateWarning, 1, 2)
        self.layout.addWidget(self.categoryLabel, 2, 0)
        self.layout.addWidget(self.categoryComboBox, 2, 1)
        self.layout.addWidget(self.descriptionLabel, 3, 0)
        self.layout.addWidget(self.descriptionLineEdit, 3, 1)
        self.layout.addWidget(self.descriptionWarning, 3, 2)
        self.layout.addWidget(self.submitButton, 4, 0, 1, 3)
        self.layout.addWidget(self.backButton, 5, 0, 1, 3)

    def load_income_categories(self):
        cursor = self.window.db.cursor
        cursor.execute("SELECT name FROM income_categories")
        categories = [row[0] for row in cursor.fetchall()]
        self.categoryComboBox.addItems(categories)

    def submit_income(self):
        amount = self.amountLineEdit.text()
        date = self.dateLineEdit.text()
        category = self.categoryComboBox.currentText()
        description = self.descriptionLineEdit.text()

        try:
            register_fine = RegisterFine(self.window.db)
            register_fine.create_tables()
            if self.window.signupLoginMenu.logining:
                register_fine.register_income(float(amount), date, category, description,self.window.signupLoginMenu.usernamelogin)
            elif self.window.signupLoginMenu.singuping:
                register_fine.register_income(float(amount), date, category, description,self.window.signupLoginMenu.user.userName)
            self.descriptionWarning.setText('Income registered successfully')
        except ValueError as e:
            self.descriptionWarning.setText(str(e))

    def back(self):
        self.amountLabel.setVisible(False)
        self.amountLineEdit.setVisible(False)
        self.amountWarning.setVisible(False)
        self.dateLabel.setVisible(False)
        self.dateLineEdit.setVisible(False)
        self.dateWarning.setVisible(False)
        self.categoryLabel.setVisible(False)
        self.categoryComboBox.setVisible(False)
        self.descriptionLabel.setVisible(False)
        self.descriptionLineEdit.setVisible(False)
        self.descriptionWarning.setVisible(False)
        self.submitButton.setVisible(False)
        self.backButton.setVisible(False)
        self.mainMenu = MainMenu(self.window)


class RegisterExpenseMenu:
    def __init__(self, window: MyWindow):
        self.window = window
        self.init_ui()

    def init_ui(self):
        self.window.signupLoginMenu.mainMenu.hide_menu()
        central_widget = QWidget(self.window)
        self.window.setCentralWidget(central_widget)
        self.layout = QGridLayout(central_widget)

        self.amountLabel = QLabel('Enter amount: ', self.window)
        self.amountLineEdit = QLineEdit(self.window)
        self.amountWarning = QLabel(' ', self.window)

        self.dateLabel = QLabel('Enter date (yyyy/mm/dd): ', self.window)
        self.dateLineEdit = QLineEdit(self.window)
        self.dateWarning = QLabel(' ', self.window)

        self.categoryLabel = QLabel('Select category: ', self.window)
        self.categoryComboBox = QComboBox(self.window)
        self.load_expense_categories()

        self.descriptionLabel = QLabel('Enter description: ', self.window)
        self.descriptionLineEdit = QLineEdit(self.window)
        self.descriptionWarning = QLabel(' ', self.window)

        self.submitButton = QPushButton('Submit', self.window)
        self.submitButton.clicked.connect(self.submit_expense)
        self.backButton = QPushButton('Back', self.window)
        self.backButton.clicked.connect(self.back)

        self.layout.addWidget(self.amountLabel, 0, 0)
        self.layout.addWidget(self.amountLineEdit, 0, 1)
        self.layout.addWidget(self.amountWarning, 0, 2)
        self.layout.addWidget(self.dateLabel, 1, 0)
        self.layout.addWidget(self.dateLineEdit, 1, 1)
        self.layout.addWidget(self.dateWarning, 1, 2)
        self.layout.addWidget(self.categoryLabel, 2, 0)
        self.layout.addWidget(self.categoryComboBox, 2, 1)
        self.layout.addWidget(self.descriptionLabel, 3, 0)
        self.layout.addWidget(self.descriptionLineEdit, 3, 1)
        self.layout.addWidget(self.descriptionWarning, 3, 2)
        self.layout.addWidget(self.submitButton, 4, 0, 1, 3)
        self.layout.addWidget(self.backButton, 5, 0, 1, 3)

    def load_expense_categories(self):
        cursor = self.window.db.cursor
        cursor.execute("SELECT name FROM expense_categories")
        categories = [row[0] for row in cursor.fetchall()]
        self.categoryComboBox.addItems(categories)

    def submit_expense(self):
        amount = self.amountLineEdit.text()
        date = self.dateLineEdit.text()
        category = self.categoryComboBox.currentText()
        description = self.descriptionLineEdit.text()

        try:
            register_fine = RegisterFine(self.window.db)
            register_fine.create_tables()
            if self.window.signupLoginMenu.logining:
                register_fine.register_income(float(amount), date, category, description,self.window.signupLoginMenu.usernamelogin)
            elif self.window.signupLoginMenu.singuping:
                register_fine.register_income(float(amount), date, category, description,self.window.signupLoginMenu.user.userName)
            self.descriptionWarning.setText('Expense registered successfully')
        except ValueError as e:
            self.descriptionWarning.setText(str(e))

    def back(self):
        self.amountLabel.setVisible(False)
        self.amountLineEdit.setVisible(False)
        self.amountWarning.setVisible(False)
        self.dateLabel.setVisible(False)
        self.dateLineEdit.setVisible(False)
        self.dateWarning.setVisible(False)
        self.categoryLabel.setVisible(False)
        self.categoryComboBox.setVisible(False)
        self.descriptionLabel.setVisible(False)
        self.descriptionLineEdit.setVisible(False)
        self.descriptionWarning.setVisible(False)
        self.submitButton.setVisible(False)
        self.backButton.setVisible(False)
        self.mainMenu = MainMenu(self.window)

class Category:
    def __init__(self, name):
        self.name = name

    def validate_name(self):
        if not self.name:
            raise ValueError("Category name cannot be empty")
        if len(self.name) > 15:
            raise ValueError(
                "Category name cannot be longer than 15 characters")
        if not re.match("^[A-Za-z0-9]*$", self.name):
            raise ValueError(
                "Category name can only contain English letters and numbers")

    def save_to_database(self, db, category_type):
        cursor = db.cursor
        cursor.execute(f"SELECT name FROM {category_type} WHERE name=?", (self.name,))
        if cursor.fetchone():
            raise ValueError("Category name already exists")
        cursor.execute(
            f"INSERT INTO {category_type} (name) VALUES (?)", (self.name,))
        db.commit()

class DataBase:
    def __init__(self):
        self.db = sqlite3.connect("ElmosBalance.db")
        self.cursor = self.db.cursor()
        self.create_data_base()

    def commit(self):
        self.db.commit()

    def create_data_base(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (first_name TEXT, last_name TEXT, national_id TEXT, phone_number TEXT, user_name TEXT PRIMARY KEY, password TEXT, city TEXT, email TEXT, birth_date TEXT, security_q_answer TEXT)")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS income_categories (name TEXT PRIMARY KEY)")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS expense_categories (name TEXT PRIMARY KEY)")


class SignupLoginMenu():
    def __init__(self, window: MyWindow):
        self.window = window
        self.singuping = False
        self.logining = False
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
            self.singuping = True
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
            self.logining = True
            self.usernamelogin=self.userNameLoginLine.text()
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
        self.backButton = QPushButton('Back', self.window)
        self.backButton.clicked.connect(self.back)

        self.layout.addWidget(self.categoryTypeLabel, 0, 0)
        self.layout.addWidget(self.categoryTypeComboBox, 0, 1)
        self.layout.addWidget(self.categoryNameLabel, 1, 0)
        self.layout.addWidget(self.categoryNameLineEdit, 1, 1)
        self.layout.addWidget(self.categoryNameWarning, 1, 2)
        self.layout.addWidget(self.submitButton, 2, 0, 1, 3)
        self.layout.addWidget(self.backButton, 3, 0, 1, 3)

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

    def back(self):
        self.categoryNameLabel.setVisible(False)
        self.categoryNameLineEdit.setVisible(False)
        self.categoryNameWarning.setVisible(False)
        self.categoryTypeComboBox.setVisible(False)
        self.categoryTypeLabel.setVisible(False)
        self.submitButton.setVisible(False)
        self.backButton.setVisible(False)
        self.mainMenu = MainMenu(self.window)

class SearchMenu:
    def __init__(self, window: MyWindow):
        self.window = window
        self.init_ui()

    def init_ui(self):
        self.window.signupLoginMenu.mainMenu.hide_menu()
        central_widget = QWidget(self.window)
        self.window.setCentralWidget(central_widget)
        self.layout = QGridLayout(central_widget)

        button_group = QButtonGroup()
        self.searchLabel=QLabel('Type for search: ',self.window)
        self.searchLine=QLineEdit(self.window)
        self.filterLabel=QLabel('filters: ',self.window)

        self.dayfilter=QRadioButton('day:',self.window)
        self.dayLine=QLineEdit(self.window)
        self.dayLine.setVisible(False)
        self.dayfilter.setAutoExclusive(False)
        button_group.addButton(self.dayfilter)
        self.dayfilter.toggled.connect(lambda checked: self.dayLine.setVisible(checked))

        self.monthfilter=QRadioButton('month:',self.window)
        self.monthLine=QLineEdit(self.window)
        self.monthLine.setVisible(False)
        self.monthfilter.setAutoExclusive(False)
        button_group.addButton(self.monthfilter)
        self.monthfilter.toggled.connect(lambda checked: self.monthLine.setVisible(checked))

        self.yearfilter=QRadioButton('year:',self.window)
        self.yearLine=QLineEdit(self.window)
        self.yearLine.setVisible(False)
        self.yearfilter.setAutoExclusive(False)
        button_group.addButton(self.yearfilter)
        self.yearfilter.toggled.connect(lambda checked: self.yearLine.setVisible(checked))

        self.incomeExpensefilter=QRadioButton('type: ',self.window)
        self.incomeExpenseCombo=QComboBox(self.window)
        self.incomeExpenseCombo.setVisible(False)
        self.incomeExpenseCombo.addItem('income')
        self.incomeExpenseCombo.addItem('expense')
        self.incomeExpenseCombo.addItem('both')
        self.incomeExpensefilter.setAutoExclusive(False)
        button_group.addButton(self.incomeExpensefilter)
        self.incomeExpensefilter.toggled.connect(lambda checked: self.incomeExpenseCombo.setVisible(checked))

        self.moneyrangefilter=QRadioButton('value range(type two number seperated by space: )',self.window)
        self.moneyrangeline=QLineEdit(self.window)
        self.moneyrangeline.setVisible(False)
        self.moneyrangefilter.setAutoExclusive(False)
        button_group.addButton(self.moneyrangefilter)
        self.moneyrangefilter.toggled.connect(lambda checked: self.moneyrangeline.setVisible(checked))

        self.searchinfilter=QRadioButton('choose the one you want to search in: ',self.window)
        self.searchinCombo=QComboBox(self.window)
        self.searchinCombo.addItem('descriptions')
        self.searchinCombo.addItem('categories')
        self.searchinCombo.addItem('both')
        self.searchinLine=QLineEdit(self.window)
        self.searchinCombo.setVisible(False)
        self.searchinLine.setVisible(False)
        self.searchinfilter.setAutoExclusive(False)
        button_group.addButton(self.searchinfilter)
        self.searchinfilter.toggled.connect(lambda checked: self.searchinCombo.setVisible(checked))
        self.searchinCombo.currentTextChanged.connect(self.searchin_func)

        self.submitButton = QPushButton('Submit', self.window)
        self.submitButton.clicked.connect(self.show_search_results)
        self.backButton = QPushButton('Back', self.window)
        self.backButton.clicked.connect(self.back)

        self.layout.addWidget(self.searchLabel,0,0)
        self.layout.addWidget(self.searchLine,0,1)
        self.layout.addWidget(self.filterLabel,1,0)
        self.layout.addWidget(self.dayfilter,2,0)
        self.layout.addWidget(self.dayLine,2,1)
        self.layout.addWidget(self.monthfilter,3,0)
        self.layout.addWidget(self.monthLine,3,1)
        self.layout.addWidget(self.yearfilter,4,0)
        self.layout.addWidget(self.yearLine,4,1)
        self.layout.addWidget(self.incomeExpensefilter,5,0)
        self.layout.addWidget(self.incomeExpenseCombo,5,1)
        self.layout.addWidget(self.moneyrangefilter,6,0)
        self.layout.addWidget(self.moneyrangeline,6,1)
        self.layout.addWidget(self.searchinfilter,7,0)
        self.layout.addWidget(self.searchinCombo,7,1)
        self.layout.addWidget(self.searchinLine,7,2)
        self.layout.addWidget(self.submitButton,8,0)
        self.layout.addWidget(self.backButton,8,1)
        self.model = QStandardItemModel(self.window)
        self.table = QTableView(self.window)
        self.table.setModel(self.model)

        self.layout.addWidget(self.table, 9, 0, 1, 2)
        self.table.hide()
    def searchin_func(self):
        if self.searchinCombo.isVisible() :
            self.searchinLine.setVisible(True) 
        else:
            self.searchinLine.setVisible(False)
    def show_search_results(self):
        self.searchengine=Search(self)
        self.searchengine.search(self.window.db)
    def back(self):
        self.searchLabel.setVisible(False)
        self.searchLine.setVisible(False)
        self.filterLabel.setVisible(False)
        self.dayfilter.setVisible(False)
        self.dayLine.setVisible(False)
        self.monthfilter.setVisible(False)
        self.monthLine.setVisible(False)
        self.yearfilter.setVisible(False)
        self.yearLine.setVisible(False)
        self.incomeExpensefilter.setVisible(False)
        self.incomeExpenseCombo.setVisible(False)
        self.moneyrangefilter.setVisible(False)
        self.moneyrangeline.setVisible(False)
        self.searchinfilter.setVisible(False)
        self.searchinCombo.setVisible(False)
        self.searchinLine.setVisible(False)
        self.submitButton.setVisible(False)
        self.backButton.setVisible(False)
        self.table.setVisible(False)
        self.mainMenu = MainMenu(self.window)
    def get_filters(self):
        self.day = self.dayLine.text()
        self.month = self.monthLine.text()
        self.year = self.yearLine.text()
        self.incomeExpense = self.incomeExpenseCombo.currentText()
        self.moneyrange = self.moneyrangeline.text()
        self.searchin= self.searchinLine.text()
        return [self.day,self.month,self.year,self.incomeExpense,self.moneyrange,self.searchin]
class Search:
    def __init__(self, menu: SearchMenu):
        self.menu = menu
        self.model=self.menu.model
        self.table=self.menu.table
    def search(self, db: DataBase):
        self.searchText = self.menu.searchLine.text()
        self.searchfilters = {
            'day': self.menu.get_filters()[0] if self.menu.get_filters()[0].strip() else None,
            'month': self.menu.get_filters()[1] if self.menu.get_filters()[1].strip() else None,
            'year': self.menu.get_filters()[2] if self.menu.get_filters()[2].strip() else None,
            'income_expense': self.menu.get_filters()[3] if self.menu.get_filters()[3].strip() else None,
            'money_range': self.menu.get_filters()[4] if self.menu.get_filters()[4].strip() else None,
            'search_in': self.menu.get_filters()[5] if self.menu.get_filters()[5].strip() else None
        }
        if self.searchfilters['income_expense'] == 'income':
            base_query = f"SELECT * FROM income_fine WHERE username='{self.menu.window.signupLoginMenu.usernamelogin if self.menu.window.signupLoginMenu.logining else self.menu.window.signupLoginMenu.user.userName}' and date LIKE '%{self.searchText}%' OR category LIKE '%{self.searchText}%' OR description LIKE '%{self.searchText}%' or amount LIKE '%{self.searchText}%'"
            self.filtering(base_query)
            db.cursor.execute(base_query)
            rows = db.cursor.fetchall()
            self.model.clear()
            self.model.setHorizontalHeaderLabels(["Amount", "Date", "Category", "Description"])
            for row in rows:
                date = QStandardItem(str(row[1]))
                category = QStandardItem(str(row[2]))
                description = QStandardItem(str(row[3]))
                amount = QStandardItem(str(row[4]))
                self.model.appendRow([date, category, description, amount])
            self.table.show()
        elif self.searchfilters['income_expense'] == 'expense':
            base_query = f"SELECT * FROM expense_fine WHERE username='{self.menu.window.signupLoginMenu.usernamelogin if self.menu.window.signupLoginMenu.logining else self.menu.window.signupLoginMenu.user.userName}' and date LIKE '%{self.searchText}%' OR category LIKE '%{self.searchText}%' OR description LIKE '%{self.searchText}%' or amount LIKE '%{self.searchText}%'"
            self.filtering(base_query)
            db.cursor.execute(base_query)
            rows = db.cursor.fetchall()
            self.model.clear()
            self.model.setHorizontalHeaderLabels(["Amount", "Date", "Category", "Description"])
            for row in rows:
                date = QStandardItem(str(row[1]))
                category = QStandardItem(str(row[2]))
                description = QStandardItem(str(row[3]))
                amount = QStandardItem(str(row[4]))
                self.model.appendRow([date, category, description, amount])
            self.table.show()
        elif self.searchfilters['income_expense'] == 'both':
            base_query1 = base_query = f"SELECT * FROM income_fine WHERE username='{self.menu.window.signupLoginMenu.usernamelogin if self.menu.window.signupLoginMenu.logining else self.menu.window.signupLoginMenu.user.userName}' and  date LIKE '%{self.searchText}%' OR category LIKE '%{self.searchText}%' OR description LIKE '%{self.searchText}%' or amount LIKE '%{self.searchText}%'"
            self.filtering(base_query1)
            db.cursor.execute(base_query1)
            base_query2 = base_query = f"SELECT * FROM expense_fine WHERE username='{self.menu.window.signupLoginMenu.usernamelogin if self.menu.window.signupLoginMenu.logining else self.menu.window.signupLoginMenu.user.userName}' and date LIKE '%{self.searchText}%' OR category LIKE '%{self.searchText}%' OR description LIKE '%{self.searchText}%' or amount LIKE '%{self.searchText}%'"
            self.filtering(base_query2)
            db.cursor.execute(base_query2)
            rows = db.cursor.fetchall()
            self.model.clear()
            self.model.setHorizontalHeaderLabels(["Amount", "Date", "Category", "Description"])
            for row in rows:
                date = QStandardItem(str(row[1]))
                category = QStandardItem(str(row[2]))
                description = QStandardItem(str(row[3]))
                amount = QStandardItem(str(row[4]))
                self.model.appendRow([date, category, description, amount])
            self.table.show()

    def filtering(self, base_query):
        for filter, value in self.searchfilters.items():
            if filter != 'income_expense' and value is not None:
                if filter == 'day' and value is not None:
                    base_query += f" AND SUBSTRING(date,9,2)='{value}'"
                elif filter == 'month' and value is not None:
                    base_query += f" AND SUBSTRING(date,6,2)='{value}'"
                elif filter == 'year' and value is not None:
                    base_query += f" AND SUBSTRING(date,1,4)='{value}'"
                elif filter == 'money_range' and value is not None:
                    value_range = value.split(sep=' ')
                    base_query += f" AND amount BETWEEN {value_range[0]} AND {value_range[1]}"
                elif filter == 'search_in' and value is not None:
                    if value == 'categories':
                        base_query += f" AND category='{value}'"
                    elif value == 'description':
                        base_query += f" AND description='{value}'"
                    elif value == 'both':
                        base_query += f" AND category='{value}' and description='{value}'"




class ReportMenu:
    def __init__(self, window: MyWindow):
        self.window = window
        self.init_ui()

    def init_ui(self):
        self.window.signupLoginMenu.mainMenu.hide_menu()
        central_widget = QWidget(self.window)
        self.window.setCentralWidget(central_widget)
        self.layout = QGridLayout(central_widget)
        button_group = QButtonGroup()

        self.reportLabel=QLabel('choose the items below to specify your report.',self.window)
        self.dayfilter=QRadioButton('day:',self.window)
        self.dayLine=QLineEdit(self.window)
        self.dayLine.setVisible(False)
        self.dayfilter.setAutoExclusive(False)
        button_group.addButton(self.dayfilter)
        self.dayfilter.toggled.connect(lambda checked: self.dayLine.setVisible(checked))

        self.monthfilter=QRadioButton('month:',self.window)
        self.monthLine=QLineEdit(self.window)
        self.monthLine.setVisible(False)
        self.monthfilter.setAutoExclusive(False)
        button_group.addButton(self.monthfilter)
        self.monthfilter.toggled.connect(lambda checked: self.monthLine.setVisible(checked))

        self.yearfilter=QRadioButton('year:',self.window)
        self.yearLine=QLineEdit(self.window)
        self.yearLine.setVisible(False)
        self.yearfilter.setAutoExclusive(False)
        button_group.addButton(self.yearfilter)
        self.yearfilter.toggled.connect(lambda checked: self.yearLine.setVisible(checked))

        self.incomeExpensefilter=QRadioButton('type: ',self.window)
        self.incomeExpenseCombo=QComboBox(self.window)
        self.incomeExpenseCombo.setVisible(False)
        self.incomeExpenseCombo.addItem('income')
        self.incomeExpenseCombo.addItem('expense')
        self.incomeExpenseCombo.addItem('both')
        self.incomeExpensefilter.setAutoExclusive(False)
        button_group.addButton(self.incomeExpensefilter)
        self.incomeExpensefilter.toggled.connect(lambda checked: self.incomeExpenseCombo.setVisible(checked))

        self.moneyrangefilter=QRadioButton('value range(type two number seperated by space: )',self.window)
        self.moneyrangeline=QLineEdit(self.window)
        self.moneyrangeline.setVisible(False)
        self.moneyrangefilter.setAutoExclusive(False)
        button_group.addButton(self.moneyrangefilter)
        self.moneyrangefilter.toggled.connect(lambda checked: self.moneyrangeline.setVisible(checked))

        self.categoryfilter=QRadioButton('please choose the category you want to search in: ',self.window)
        self.categoryline=QLineEdit(self.window)
        self.categoryline.setVisible(False)
        self.categoryfilter.setAutoExclusive(False)
        button_group.addButton(self.categoryfilter)
        self.categoryfilter.toggled.connect(lambda checked: self.categoryline.setVisible(checked))

        self.submitButton = QPushButton('Submit', self.window)
        self.submitButton.clicked.connect(self.show_search_results)
        self.backButton = QPushButton('Back', self.window)
        self.backButton.clicked.connect(self.back)

        self.layout.addWidget(self.reportLabel,0,0)
        self.layout.addWidget(self.dayfilter,1,0)
        self.layout.addWidget(self.dayLine,1,1)
        self.layout.addWidget(self.monthfilter,2,0)
        self.layout.addWidget(self.monthLine,2,1)
        self.layout.addWidget(self.yearfilter,3,0)
        self.layout.addWidget(self.yearLine,3,1)
        self.layout.addWidget(self.incomeExpensefilter,4,0)
        self.layout.addWidget(self.incomeExpenseCombo,4,1)
        self.layout.addWidget(self.moneyrangefilter,5,0)
        self.layout.addWidget(self.moneyrangeline,5,1)
        self.layout.addWidget(self.categoryfilter,6,0)
        self.layout.addWidget(self.categoryline,6,1)
        self.layout.addWidget(self.submitButton,7,0)
        self.layout.addWidget(self.backButton,7,1)
        self.model = QStandardItemModel(self.window)
        self.table = QTableView(self.window)
        self.table.setModel(self.model)

        self.layout.addWidget(self.table, 8, 0, 1, 2)
        self.table.hide()
    def back(self):
        self.reportLabel.setVisible(False)
        self.dayfilter.setVisible(False)
        self.dayLine.setVisible(False)
        self.monthfilter.setVisible(False)
        self.monthLine.setVisible(False)
        self.yearfilter.setVisible(False)
        self.yearLine.setVisible(False)
        self.incomeExpensefilter.setVisible(False)
        self.incomeExpenseCombo.setVisible(False)
        self.moneyrangefilter.setVisible(False)
        self.moneyrangeline.setVisible(False)
        self.categoryfilter.setVisible(False)
        self.categoryline.setVisible(False)
        self.submitButton.setVisible(False)
        self.backButton.setVisible(False)
        self.table.setVisible(False)
        self.mainMenu = MainMenu(self.window)
    def show_search_results(self):
        self.reportEngine=Report(self)
        self.reportEngine.search(self.window.db)
    def get_filters(self):
        self.day = self.dayLine.text()
        self.month = self.monthLine.text()
        self.year = self.yearLine.text()
        self.incomeExpense = self.incomeExpenseCombo.currentText()
        self.moneyrange = self.moneyrangeline.text()
        self.searchin= self.categoryline.text()
        return [self.day,self.month,self.year,self.incomeExpense,self.moneyrange,self.searchin]
class Report:
    def __init__(self, menu: ReportMenu):
        self.menu = menu
        self.model=self.menu.model
        self.table=self.menu.table
    def search(self, db: DataBase):
        self.searchfilters = {
            'day': self.menu.get_filters()[0] if self.menu.get_filters()[0].strip() else None,
            'month': self.menu.get_filters()[1] if self.menu.get_filters()[1].strip() else None,
            'year': self.menu.get_filters()[2] if self.menu.get_filters()[2].strip() else None,
            'income_expense': self.menu.get_filters()[3] if self.menu.get_filters()[3].strip() else None,
            'money_range': self.menu.get_filters()[4] if self.menu.get_filters()[4].strip() else None,
            'search_in': self.menu.get_filters()[5] if self.menu.get_filters()[5].strip() else None
        }
        if self.searchfilters['income_expense'] == 'income':
            base_query = f"SELECT * FROM income_fine WHERE username='{self.menu.window.signupLoginMenu.usernamelogin if self.menu.window.signupLoginMenu.logining else self.menu.window.signupLoginMenu.user.userName}'"
            self.filtering(base_query)
            db.cursor.execute(base_query)
            rows = db.cursor.fetchall()
            self.model.clear()
            self.model.setHorizontalHeaderLabels(["Amount", "Date", "Category", "Description"])
            for row in rows:
                date = QStandardItem(str(row[1]))
                category = QStandardItem(str(row[2]))
                description = QStandardItem(str(row[3]))
                amount = QStandardItem(str(row[4]))
                self.model.appendRow([date, category, description, amount])
            self.table.show()
        elif self.searchfilters['income_expense'] == 'expense':
            base_query = f"SELECT * FROM expense_fine WHERE username='{self.menu.window.signupLoginMenu.usernamelogin if self.menu.window.signupLoginMenu.logining else self.menu.window.signupLoginMenu.user.userName}'"
            self.filtering(base_query)
            db.cursor.execute(base_query)
            rows = db.cursor.fetchall()
            self.model.clear()
            self.model.setHorizontalHeaderLabels(["Amount", "Date", "Category", "Description"])
            for row in rows:
                date = QStandardItem(str(row[1]))
                category = QStandardItem(str(row[2]))
                description = QStandardItem(str(row[3]))
                amount = QStandardItem(str(row[4]))
                self.model.appendRow([date, category, description, amount])
            self.table.show()
        elif self.searchfilters['income_expense'] == 'both':
            base_query1 = base_query = f"SELECT * FROM income_fine WHERE username='{self.menu.window.signupLoginMenu.usernamelogin if self.menu.window.signupLoginMenu.logining else self.menu.window.signupLoginMenu.user.userName}'"
            self.filtering(base_query1)
            db.cursor.execute(base_query1)
            base_query2 = base_query = f"SELECT * FROM expense_fine WHERE username='{self.menu.window.signupLoginMenu.usernamelogin if self.menu.window.signupLoginMenu.logining else self.menu.window.signupLoginMenu.user.userName}'"
            self.filtering(base_query2)
            db.cursor.execute(base_query2)
            rows = db.cursor.fetchall()
            self.model.clear()
            self.model.setHorizontalHeaderLabels(["Amount", "Date", "Category", "Description"])
            for row in rows:
                date = QStandardItem(str(row[1]))
                category = QStandardItem(str(row[2]))
                description = QStandardItem(str(row[3]))
                amount = QStandardItem(str(row[4]))
                self.model.appendRow([date, category, description, amount])
            self.table.show()

    def filtering(self, base_query):
        for filter, value in self.searchfilters.items():
            if filter != 'income_expense' and value is not None:
                if filter == 'day' and value is not None:
                    base_query += f" AND DAY(DATE(date))='{value}'"
                elif filter == 'month' and value is not None:
                    base_query += f" MONTH(DATE(date))='{value}'"
                elif filter == 'year' and value is not None:
                    base_query += f" AND YEAR(DATE(date))='{value}'"
                elif filter == 'money_range' and value is not None:
                    value_range = value.split(sep=' ')
                    base_query += f" AND amount BETWEEN {value_range[0]} AND {value_range[1]}"
                elif filter == 'search_in' and value is not None:
                        base_query += f" AND category='{value}'"

class MainMenu():
    def __init__(self, window: MyWindow):
        self.window = window
        self.show_main_menu()

    def register_income(self):
        self.hide_menu()
        self.registerIncomeMenu=RegisterIncomeMenu(self.window)

    def register_expense(self):
        self.hide_menu()
        self.registerIncomeMenu=RegisterExpenseMenu(self.window)

    def show_categories(self):
        self.hide_menu()
        self.categoryMenu = CategoryMenu(self.window)

    def show_search(self):
        self.hide_menu()
        self.searchMenu = SearchMenu(self.window)

    def show_reporting(self):
        self.hide_menu()
        self.reportMenu = ReportMenu(self.window)

    def show_settings(self):
        self.hide_menu()

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
