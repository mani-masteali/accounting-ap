import time
from rich.console import Console
from rich.text import Text
from colors import blue, red, green, yellow, purple, cyan, magenta, white, black, gray
import msvcrt
from registerFine import RegisterFine
from category import Category
from search import Search
from report import Report
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
                    self.selectedOption = (self.selectedOption - 1) % len(self.options)
                elif keyCode == 80:  # Down arrow key
                    self.selectedOption = (self.selectedOption + 1) % len(self.options)
                self.display_menu()
            elif key == b'\r':  # Enter key
                time.sleep(1)
                return self.options[self.selectedOption]
            elif key == b'q':  # 'q' key
                exit()
            elif key.isdigit():  # If a digit is pressed
                optionNum = int(key)
                if 1 <= optionNum <= len(self.options):
                    self.selectedOption = optionNum - 1
                    self.display_menu()
                    time.sleep(1)
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

if __name__ == "__main__":
    menu=FirstMenu()
    menu.show_menu()
    option=input()
    if option=='1':
        while True:
            userX=User()
            try:
                userX.get_first_name(input('first name: '))
                userX.get_last_name(input('last name: '))
                userX.get_code_meli(input('national id: '))
                userX.get_phone_number(input('mobile number: '))
                userX.get_username(input('user name: '))
                userX.get_password(pwinput.pwinput(prompt='enter password:'))
                userX.check_repeated_password(pwinput.pwinput(prompt='confrim password:'))
                userX.get_city(str(Console().input(f'[bold white] please choose the city from this list: [cyan] {userX.savedcities} \n :')))
                userX.get_email(input('email: '))
                userX.get_birth_date(input('birth date: (yyyy/mm/dd) '))
                userX.get_security_questions_answer(input('What is your favorite car brand? '))
                userX.save_csv()
                last_option=str(Console().input('[green] type submit to continue\n'))
                if last_option=='submit':
                    Console().print('[bold green] welcome to the app!')
                    time.sleep(2)
                    break
                else:
                    Console().print('[bold red] Invalid input')
            except ValueError as error:
                print(error)
    elif option=='2':
        count=0
        while True:
            userName=input('username: ')
            password=pwinput.pwinput(prompt='password: ')
            if login_user(userName,password)==True:
                Console().print(Text('login was succesful!'),style=green)
                time.sleep(2)
                break
            else:
                Console().print(Text('username or password is wrong or does not exist!'),style=red)
                count+=1
                count_wrong_enters(count)
                forgotOrNot=input('forgot your password? ')
                if forgotOrNot=='Yes' or forgotOrNot=='yes':
                    userNameOrEmail=input('enter your username or email: ')
                    securityQAnswer=input('What is your favorite car brand? ')
                    forgot_password(userNameOrEmail,securityQAnswer)
    startTime = time.time()  # Start menu and app usage time recording
    menu = MainMenu()
    register = RegisterFine()
    category = Category()
    while True:
        menu.display_menu()
        selectedOptionName = menu.handle_input()
        if selectedOptionName == menu.options[0]:
            register.registerIncome()
        elif selectedOptionName == menu.options[1]:
            register.registerExpense()
        elif selectedOptionName == menu.options[2]:
            result = category.display_category_menu()
            if result == "Main menu":
                register = RegisterFine()
                category = Category()
                continue
        elif selectedOptionName == menu.options[3]:
            print("Search")
            time.sleep(2)  # Placeholder for search functionality
            searchEngine=Search()
            searchEngine.show_search_filters()
            searchEngine.show_search_results()
            #an option to make the menu stationary until the users demands for exit
            if searchEngine.back_to_the_main_menu()=='Main Window':
                continue
        elif selectedOptionName == menu.options[4]:
            print("Reporting")
            time.sleep(2)  # Placeholder for reporting functionality
            reportCard=Report()
            reportCard.show_search_filters()
            reportCard.show_search_results()
            time.sleep(20)
        elif selectedOptionName == menu.options[5]:
            print("Settings")
            time.sleep(20)  # Placeholder for settings functionality
        elif selectedOptionName == menu.options[6]:
            exit()
