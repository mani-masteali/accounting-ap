import time
from rich.console import Console
from rich.text import Text
from colors import blue, red, green, yellow, purple, cyan, magenta, white, black, gray
import sys
import msvcrt
from registerFine import RegisterFine
from category import Category
from search import Search
from report import Report
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
        Console().print(Text("Main Menu:", style=cyan))
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
            elif key == b'\r':  # Enter key
                time.sleep(1)
                return self.options[self.selectedOption]
            elif key == b'q':  # 'q' key
                self.exit()
            elif key.isdigit():  # If a digit is pressed
                optionNum = int(key)
                if 1 <= optionNum <= len(self.options):
                    return self.options[optionNum - 1]
                else:
                    raise ValueError("Number out of range")
            else:
                raise ValueError("Invalid input")
        except ValueError as e:
            self.display_menu(str(e))
            # Pause to show the error message and then get input again if our input value was not valid.
            time.sleep(3)
        except Exception as e:
            Console().print(Text(f"An unexpected error occurred: {e}", style=red))
            return None

    def exit(self):
        endTime = time.time()
        Console().print(Text("Total time:", style=yellow), Text(f"{endTime - startTime:.2f}", style=purple), Text("seconds", style=yellow))
        Console().print(Text("Exiting ...", style=magenta))
        time.sleep(1)
        sys.exit()

if __name__ == "__main__":
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
            register.registerCost()
        elif selectedOptionName == menu.options[2]:
            category.display_category_menu()
        elif selectedOptionName == menu.options[3]:
            print("Search")
            time.sleep(2)
            Search.show_search_filters()
        elif selectedOptionName == menu.options[4]:
            print("Reporting")
            time.sleep(2)
            Report.show_search_filters()
        elif selectedOptionName == menu.options[5]:
            print("Settings")
            time.sleep(2)  # by Mani
        elif selectedOptionName == menu.options[6]:
            menu.exit()
