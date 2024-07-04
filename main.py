import time
from rich.console import Console
from rich.text import Text
from colors import blue, red, green, yellow, purple, cyan, magenta, white, black, gray
import msvcrt
from registerFine import RegisterFine
from category import Category
from search import Search
from report import Report
from setting import Setting
from exit import exit
from login_and_signup_menu import FirstMenu
import pwinput
from login import *
from signup import *


class MainMenu():
    def __init__(self):
        self.options = [
            "Register Income",
            "Register Expense",
            "Categories",
            "Search",
            "Reporting",
            "Settings",
            "Exit"
        ]
        self.selectedOption = 0

    def display_menu(self, errorMessage=None):
        Console().clear()
        Console().print(Text("Main Menu:", style=blue))
        Console().print(Text("Press arrow keys and enter button or press the number of your choice (range 1-7). Press 'q' to exit.", style=gray))
        if errorMessage:
            Console().print(Text(f"Error: {errorMessage}", style=red))
        for i, option in enumerate(self.options):
            if i == self.selectedOption:
                Console().print(Text(f"-> {i + 1}- {option}", style=blue))
            else:
                Console().print(Text(f"   {i + 1}- {option}", style=cyan))

    def handle_input(self):
        try:
            key = msvcrt.getch()
            if key == b'\xe0':  # Arrow keys are preceded by '\xe0'. if this condition not checked, we will get an invalid input error when using arrow keys
                keyCode = ord(msvcrt.getch())
                if keyCode == 72:  # Up arrow key
                    self.selectedOption = (
                        self.selectedOption - 1) % len(self.options)
                elif keyCode == 80:  # Down arrow key
                    self.selectedOption = (
                        self.selectedOption + 1) % len(self.options)
                self.display_menu()
            elif key == b'\r':  # Enter key
                time.sleep(1)
                return self.options[self.selectedOption]
            elif key == b'q':  # 'q' key
                startTime
            elif key.isdigit():  # If a digit is pressed
                optionNum = int(key)
                if 1 <= optionNum <= len(self.options):
                    self.selectedOption = optionNum - 1
                    self.display_menu()
                    return self.options[self.selectedOption]
                else:
                    raise ValueError("Number out of range")
            else:
                raise ValueError("Invalid input")
        except ValueError as e:
            self.display_menu(str(e))
            # Pause to show the error message and then get input again if our input value was not valid.
            time.sleep(3)
        except Exception as e:
            Console().print(
                Text(f"An unexpected error occurred: {e}", style=red))
            return None


def get_input_with_retry(prompt, validate, style=blue, errorStyle=red):
    while True:
        if "password" in prompt.lower():
            value = pwinput.pwinput(prompt)
        else:
            value = Console().input(Text(prompt, style=style))

        try:
            validate(value)
            return value
        except ValueError as e:
            pass


if __name__ == "__main__":
    menu = FirstMenu()

    option = menu.show_menu()

    if option == 1:
        firstName = lastName = nationalId = phoneNumber = userName = password = confirmedPassword = city = email = birthDate = securityAnswer = None
        while True:
            userX = User()
            try:
                if not firstName:
                    firstName = get_input_with_retry(
                        "First name: ", userX.get_first_name)
                if not lastName:
                    lastName = get_input_with_retry(
                        "Last name: ", userX.get_last_name)
                if not nationalId:
                    nationalId = get_input_with_retry(
                        "National ID: ", userX.get_code_meli)
                if not phoneNumber:
                    phoneNumber = get_input_with_retry(
                        "Mobile number: ", userX.get_phone_number)
                if not userName:
                    userName = get_input_with_retry(
                        "User name: ", userX.get_username)
                if not password:
                    password = get_input_with_retry(
                        'Enter password: ', userX.get_password)
                if not confirmedPassword:
                    confirmedPassword = get_input_with_retry(
                        'Confirm password: ', userX.check_repeated_password)
                if not city:
                    city = get_input_with_retry(f'Please choose your city from this list:\n{userX.savedcities} \n :', userX.get_city)
                if not email:
                    email = get_input_with_retry("Email: ", userX.get_email)
                if not birthDate:
                    birthDate = get_input_with_retry(
                        "Birthday (yyyy/mm/dd) : ", userX.get_birth_date)
                if not securityAnswer:
                    securityAnswer = get_input_with_retry(
                        "What is your favorite car brand? ", userX.get_security_questions_answer)

                userX.save_csv()
                Console().print(Text('Press enter button to continue:\n', style=yellow))
                lastOption  = msvcrt.getch()
                if lastOption == b'\r':
                    Console().print(Text("Welcome to the app!", style=green))
                    time.sleep(2)
                    break
                else:
                    Console().print(Text("Invalid input", style=red))
            except ValueError as error:
                Console().print(Text(str(error), style=red))
                time.sleep(2)

    elif option == 2:
        count = 0
        while True:
            userName = Console().input(Text("Username: ", style=blue))
            password = pwinput.pwinput(prompt='Password: ')
            if login_user(userName, password):
                Console().print(Text('Login was successful!', style=green))
                time.sleep(2)
                break
            else:
                Console().print(Text('Username or password is wrong or does not exist!', style=red))
                count += 1
                count_wrong_enters(count)
                forgotOrNot = Console().input(Text("Forgot your password? (yes/no): ", style=blue))
                if forgotOrNot.lower() == 'yes':
                    userNameOrEmail = Console().input(
                        Text("Enter your username or email: ", style=blue))
                    securityQAnswer = Console().input(
                        Text("What is your favorite car brand? ", style=blue))
                    forgot_password(userNameOrEmail, securityQAnswer)

    startTime = time.time()  # Start menu and app usage time recording
    menu = MainMenu()
    register = RegisterFine()
    category = Category(startTime)
    setting = Setting(startTime,userName)
    while True:
        menu.display_menu()
        selectedOptionName = menu.handle_input()
        if selectedOptionName == "Exit":
            exit(startTime)
            break
        elif selectedOptionName == menu.options[0]:
            register.registerIncome()
        elif selectedOptionName == menu.options[1]:
            register.registerExpense()
        elif selectedOptionName == menu.options[2]:
            result = category.display_category_menu()
            if result == "Main menu":
                register = RegisterFine()
                category = Category(startTime)
                continue
        elif selectedOptionName == menu.options[3]:
            time.sleep(2)  # Placeholder for search functionality
            searchEngine = Search()
            searchEngine.show_search_filters()
            searchEngine.show_search_results()
            # an option to make the menu stationary until the users demands for exit
            if searchEngine.back_to_the_main_menu() == 'Main Window':
                continue
        elif selectedOptionName == menu.options[4]:
            time.sleep(2)  # Placeholder for reporting functionality
            reportCard = Report()
            reportCard.show_search_filters()
            reportCard.show_search_results()
            time.sleep(20)
        elif selectedOptionName == menu.options[5]:
            result = setting.display_menu()
            if result == "Main menu":
                register = RegisterFine()
                category = Category(startTime)
                setting = Setting(startTime,userName)
                continue
