from colors import green, blue, cyan, red
from rich.console import Console
from rich.text import Text
from signup import User
from login import login_user, count_wrong_enters, forgot_password
import msvcrt
import time


class FirstMenu:
    def __init__(self):
        self.menuOptions = ['Sign up', 'Log in']
        self.selectedOption = 0

    def show_menu(self):
        while True:
            Console().clear()
            Console().print(Text('Welcome to the accounting management app!', style=blue))
            Console().print(Text(r"""     
░█▀█░█▀▀░█▀▄░█▀▀░█▀█░█▀█░█▀█░█░░░░░█▀█░█▀▀░█▀▀░█▀█░█░█░█▀█░▀█▀░▀█▀░█▀█░█▀▀
░█▀▀░█▀▀░█▀▄░▀▀█░█░█░█░█░█▀█░█░░░░░█▀█░█░░░█░░░█░█░█░█░█░█░░█░░░█░░█░█░█░█
░▀░░░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀░▀▀▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░▀▀▀
""", style=blue))

            Console().print(Text('Please choose your option (press Enter to select):', style=green))
            for i, option in enumerate(self.menuOptions):
                if i == self.selectedOption:
                    Console().print(Text(f'-> {i + 1}- {option}', style=blue))
                else:
                    Console().print(Text(f'   {i + 1}- {option}', style=cyan))

            try:
                key = msvcrt.getch()
                if key == b'\xe0':  # Arrow keys are preceded by '\xe0'
                    keyCode = ord(msvcrt.getch())
                    if keyCode == 72:  # Up arrow key
                        self.selectedOption = (
                            self.selectedOption - 1) % len(self.menuOptions)
                    elif keyCode == 80:  # Down arrow key
                        self.selectedOption = (
                            self.selectedOption + 1) % len(self.menuOptions)
                elif key == b'\r':  # Enter key
                    return self.selectedOption + 1
                elif key.isdigit():  # If a digit is pressed
                    optionNum = int(key)
                    time.sleep(1)
                    if 1 <= optionNum <= len(self.menuOptions):
                        return optionNum
                    else:
                        raise ValueError("Number out of range")
                else:
                    raise ValueError("Invalid input")
            except ValueError as e:
                Console().print(Text(f"Error: {e}", style=red))
                time.sleep(2)
            except Exception as e:
                Console().print(
                    Text(f"An unexpected error occurred: {e}", style=red))
                return None
