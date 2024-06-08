import csv
import time
from rich.console import Console
from rich.text import Text
import msvcrt
import subprocess
import sys
from exit import exit  # Assuming exit is in a file named exit.py

class Setting:
    def __init__(self, startTime, userName):
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
        self.userName = userName

    def load_user_details(self):
        try:
            with open('users.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['userName'] == self.userName:
                        return row
            raise ValueError("User details not found")
        except Exception as e:
            Console().print(Text(f"Failed to load user details: {e}", style="red"))
            return None

    def change_user_profile(self):
        userDetails = self.load_user_details()
        if userDetails:
            optionMenu = [
                "First Name",
                "Last Name",
                "Phone Number",
                "Password",
                "City",
                "Email",
                "Birth Date",
                "Back"
            ]
            fieldMap = {
                "First Name": "firstName",
                "Last Name": "lastName",
                "Phone Number": "phoneNumber",
                "Password": "password",
                "City": "city",
                "Email": "email",
                "Birth Date": "birthDate"
            }
            selectedOption = 0

            while True:
                Console().clear()
                Console().print(Text("Choose an option to change:", style="blue"))
                for i, option in enumerate(optionMenu):
                    if i == selectedOption:
                        Console().print(Text(f"-> {i + 1}- {option}", style="blue"))
                    else:
                        Console().print(Text(f"   {i + 1}- {option}", style="cyan"))

                key = msvcrt.getch()
                if key == b'\xe0':
                    keyCode = ord(msvcrt.getch())
                    if keyCode == 72:
                        selectedOption = (selectedOption - 1) % len(optionMenu)
                    elif keyCode == 80:
                        selectedOption = (selectedOption + 1) % len(optionMenu)
                elif key == b'\r':
                    selectedOptionName = optionMenu[selectedOption]
                    if selectedOptionName == "Back":
                        return
                    else:
                        Console().clear()
                        Console().print(Text(f"Enter new {selectedOptionName}: ", style="yellow"))
                        newValue = input()
                        csv_field = fieldMap[selectedOptionName]
                        userDetails[csv_field] = newValue
                        self.save_user_details(userDetails)
                        Console().print(Text("User profile updated successfully.", style="green"))
                        time.sleep(2)
                elif key == b'q':
                    return
                elif key.isdigit():
                    optionNum = int(key)
                    if 1 <= optionNum <= len(optionMenu):
                        selectedOptionName = optionMenu[optionNum - 1]
                        if selectedOptionName == "Back":
                            return
                        else:
                            Console().print(Text(f"Enter new {selectedOptionName}: ", style="yellow"))
                            newValue = input()
                            csv_field = fieldMap[selectedOptionName]
                            userDetails[csv_field] = newValue
                            self.save_user_details(userDetails)
                            Console().print(Text("User profile updated successfully.", style="green"))
                            time.sleep(2)
                    else:
                        Console().print(Text("Number out of range", style="red"))
                        time.sleep(2)
                else:
                    Console().print(Text("Invalid input", style="red"))
                    time.sleep(2)

    def save_user_details(self, userDetails):
        try:
            with open('users.csv', 'r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            with open('users.csv', 'w', newline='') as file:
                fieldnames = ['firstName', 'lastName', 'nationalId', 'phoneNumber', 'userName', 'password', 'city', 'email', 'birthDate', 'SecurityQAnswer']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in rows:
                    if row['userName'] == self.userName:
                        for key in userDetails:
                            row[key] = userDetails[key]
                    writer.writerow(row)
        except Exception as e:
            Console().print(Text(f"Failed to save user details: {e}", style="red"))

    def display_menu(self, errorMessage=None):
        while True:
            Console().clear()
            Console().print(Text("Setting:", style="blue"))
            Console().print(Text("Press arrow keys and enter button or press the number of your choice (range 1-6). Press 'q' to exit.", style="gray"))
            if errorMessage:
                Console().print(Text(f"Error: {errorMessage}", style="red"))
            for i, option in enumerate(self.options):
                if i == self.selectedOption:
                    Console().print(Text(f"-> {i + 1}- {option}", style="blue"))
                else:
                    Console().print(Text(f"   {i + 1}- {option}", style="cyan"))

            key = msvcrt.getch()
            if key == b'\xe0':
                keyCode = ord(msvcrt.getch())
                if keyCode == 72:
                    self.selectedOption = (self.selectedOption - 1) % len(self.options)
                elif keyCode == 80:
                    self.selectedOption = (self.selectedOption + 1) % len(self.options)
            elif key == b'\r':
                selectedOption = self.options[self.selectedOption]
                if selectedOption == self.options[0]:
                    self.change_user_profile()
                elif selectedOption == self.options[1]:
                    self.delete_user_profile()
                    time.sleep(2)
                elif selectedOption == self.options[2]:
                    self.clear_csv('income.csv')
                elif selectedOption == self.options[3]:
                    self.clear_csv('expense.csv')
                elif selectedOption == self.options[4]:
                    return "Main menu"
                elif selectedOption == self.options[5]:
                    exit(self.startTime)
            elif key == b'q':
                exit(self.startTime)
            elif key.isdigit():
                optionNum = int(key)
                if 1 <= optionNum <= len(self.options):
                    selectedOption = self.options[optionNum - 1]
                    if selectedOption == self.options[0]:
                        self.change_user_profile()
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
                    self.display_menu("Number out of range")
                    time.sleep(2)
            else:
                self.display_menu("Invalid input")
                time.sleep(2)

    def clear_csv(self, fileName):
        try:
            with open(fileName, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)
            with open(fileName, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
            Console().print(Text(f"Data in {fileName} has been cleared.", style="green"))
        except Exception as e:
            Console().print(Text(f"Failed to clear data in {fileName}: {e}", style="red"))

    def delete_user_profile(self):
        try:
            with open('users.csv', 'r') as file:
                lines = file.readlines()
            with open('users.csv', 'w') as file:
                for line in lines:
                    if self.userName in line:
                        continue
                    file.write(line)
            Console().print(Text(f"User profile for '{self.userName}' deleted successfully. We are logging out ...", style="green"))
        except Exception as e:
            Console().print(Text(f"Failed to delete user profile: {e}", style="red"))
