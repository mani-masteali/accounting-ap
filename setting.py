import time
import sys
import csv
from rich.console import Console
from rich.text import Text
from colors import blue, red, green, yellow, purple, cyan, magenta, white, black, gray
import msvcrt
from exit import exit
import subprocess

class Setting():
    def __init__(self, startTime,userName):
        self.options = [
            "Change user profile",
            "Delete user Profile",
            "Delete incomes",
            "Delete expenses",
            "Main menu",
            "Exit"
        ]
        self.selectedOption = 0
        self.startTime = startTime
        self.userName=userName
    def display_menu(self, errorMessage=None):
        console = Console()
        while True:
            console.clear()
            console.print(Text("Setting:", style=blue))
            console.print(Text("Press arrow keys and enter button or press the number of your choice (range 1-6). Press 'q' to exit.", style=gray))
            if errorMessage:
                console.print(Text(f"Error: {errorMessage}", style=red))
            for i, option in enumerate(self.options):
                if i == self.selectedOption:
                    console.print(Text(f"-> {i + 1}- {option}", style=blue))
                else:
                    console.print(Text(f"   {i + 1}- {option}", style=cyan))
            try:
                key = msvcrt.getch()
                if key == b'\xe0':  # Arrow keys are preceded by '\xe0'
                    keyCode = ord(msvcrt.getch())
                    if keyCode == 72:  # Up arrow key
                        self.selectedOption = (self.selectedOption - 1) % len(self.options)
                    elif keyCode == 80:  # Down arrow key
                        self.selectedOption = (self.selectedOption + 1) % len(self.options)
                elif key == b'\r':  # Enter key
                    selectedOption = self.options[self.selectedOption]
                    if selectedOption == self.options[0]:
                        pass
                    elif selectedOption == self.options[1]:
                        self.delete_user_profile()
                        time.sleep(2)
                    elif selectedOption == self.options[2]:
                        self.clear_csv('income.csv')
                        time.sleep(2)

                    elif selectedOption == self.options[3]:
                        self.clear_csv('expense.csv')
                        time.sleep(2)
                    elif selectedOption == self.options[4]:
                        return "Main menu"
                    elif selectedOption == self.options[5]:
                        exit(self.startTime)
                elif key == b'q':  # 'q' key
                    exit(self.startTime)
                elif key.isdigit():  # If a digit is pressed
                    optionNum = int(key)
                    if 1 <= optionNum <= len(self.options):
                        selectedOption = self.options[optionNum - 1]
                        if selectedOption == self.options[0]:
                            pass
                        elif selectedOption == self.options[1]:
                            self.delete_user_profile()
                            time.sleep(2)
                            subprocess.run(["python", "main.py"])

                        elif selectedOption == self.options[2]:
                            self.clear_csv('income.csv')
                        elif selectedOption == self.options[3]:
                            self.clear_csv('expense.csv')
                        elif selectedOption == self.options[4]:
                            return "Main menu"
                        elif selectedOption == self.options[5]:
                            exit(self.startTime)
                    else:
                        raise ValueError("Number out of range")
                else:
                    raise ValueError("Invalid input")
            except ValueError as e:
                self.display_menu(str(e))
                # Pause to show the error message and then get input again if our input value was not valid.
                time.sleep(2)
            except Exception as e:
                console.print(Text(f"An unexpected error occurred: {e}", style=red))
                return None
        
    def clear_csv(self, fileName):
        try:
            with open(fileName, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)  
            
            with open(fileName, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header) 
            
            Console().print(Text(f"Data in {fileName} has been cleared.", style=green))
        except Exception as e:
            Console().print(Text(f"Failed to clear data in {fileName}: {e}", style=red))
    def delete_user_profile(self):
        try:
            with open('users.csv', 'r') as file:
                lines = file.readlines()
            with open('users.csv', 'w') as file:
                for line in lines:
                    # Check if the logged-in user's username is in the line
                    if self.userName in line:
                        continue  # Skip writing this line
                    file.write(line)
            Console().print(Text(f"User profile for '{self.userName}' deleted successfully. We are logging out ...", style=green))
        except Exception as e:
            Console().print(Text(f"Failed to delete user profile: {e}", style=red))
