import re
import msvcrt
import time
from rich.console import Console
from rich.text import Text
from colors import blue, red, gray, cyan, yellow, green
from exit import exit

class Category:
    def __init__(self, startTime, incomeFile="incomeCategories.txt", expenseFile="expenseCategories.txt"):
        self.startTime = startTime
        self.incomeFile = incomeFile
        self.expenseFile = expenseFile
        self.incomeCategories = self.load_categories(self.incomeFile)
        self.expenseCategories = self.load_categories(self.expenseFile)
        self.categoriesMenuOptions = [
            "Add income category", "Add expense category", "Main menu", "Exit"]
        self.categoriesMenuSelectedOption = 0

    def load_categories(self, file):
        try:
            with open(file, mode='r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []

    def save_categories(self, file, categories):
        with open(file, mode='w') as f:
            for cat in categories:
                f.write(cat + "\n")

    def add_category(self, categoryType):
        while True:
            category = Console().input(Text(f"Enter new {categoryType} category name: ", style=cyan)).capitalize()
            if self.is_category_valid(category):
                if categoryType == "income":
                    if category in self.incomeCategories:
                        Console().print(Text(f"Income category '{category}' already exists."), style=yellow)
                    else:
                        self.incomeCategories.append(category)
                        self.save_categories(self.incomeFile, self.incomeCategories)
                        Console().print(Text(f"Income category '{category}' added successfully.", style=green, no_wrap=True))
                elif categoryType == "expense":
                    if category in self.expenseCategories:
                        Console().print(Text(f"Expense category '{category}' already exists.", style=yellow))
                    else:
                        self.expenseCategories.append(category)
                        self.save_categories(self.expenseFile, self.expenseCategories)
                        Console().print(Text(f"Expense category '{category}' added successfully.", style=green, no_wrap=True))
                break

    def is_category_valid(self, category):
        if not category:
            Console.print(Text("Category name cannot be empty.", style=red))
            return False
        if len(category) > 15:
            Console.print(Text("Category name must be 15 characters or less.", style=red))
            return False
        if not re.match("^[A-Za-z0-9]+$", category):
            Console.print(Text("Category name must contain only letters and numbers.", style=red))
            return False
        return True

    def display_category_menu(self, errorMessage=None):
        while True:
            Console().clear()
            Console().print(Text("Options:", style=cyan))
            Console().print(Text("Press arrow keys and enter button or press the number of your choice (range 1-4). Press 'q' to exit.", style=gray))
            if errorMessage:
                Console().print(Text(f"Error: {errorMessage}", style=red))
            for i, option in enumerate(self.categoriesMenuOptions):
                if i == self.categoriesMenuSelectedOption:
                    Console().print(Text(f"-> {i + 1}- {option}", style=blue))
                else:
                    Console().print(Text(f"   {i + 1}- {option}", style=cyan))

            # Display the income and expense categories
            Console().print(Text("\nIncome Categories:", style=cyan))
            for cat in self.incomeCategories:
                Console().print(Text(f"- {cat}", style=cyan))

            Console().print(Text("\nExpense Categories:", style=cyan))
            for cat in self.expenseCategories:
                Console().print(Text(f"- {cat}", style=cyan))

            try:
                key = msvcrt.getch()
                if key == b'\xe0':  # Arrow keys are preceded by '\xe0'
                    keyCode = ord(msvcrt.getch())
                    if keyCode == 72:  # Up arrow key
                        self.categoriesMenuSelectedOption = (self.categoriesMenuSelectedOption - 1) % len(self.categoriesMenuOptions)
                    elif keyCode == 80:  # Down arrow key
                        self.categoriesMenuSelectedOption = (self.categoriesMenuSelectedOption + 1) % len(self.categoriesMenuOptions)
                elif key == b'\r':  # Enter key
                    selectedOption = self.categoriesMenuOptions[self.categoriesMenuSelectedOption]
                    if selectedOption == "Add income category":
                        self.add_category("income")
                    elif selectedOption == "Add expense category":
                        self.add_category("expense")
                    elif selectedOption == "Main menu":
                        return "Main menu"
                    elif selectedOption == "Exit":
                        exit(self.startTime)
                elif key == b'q':  # 'q' key
                    exit(self.startTime)
                elif key.isdigit():  # If a digit is pressed
                    optionNum = int(key)
                    if 1 <= optionNum <= len(self.categoriesMenuOptions):
                        selectedOption = self.categoriesMenuOptions[optionNum - 1]
                        if selectedOption == "Add income category":
                            self.add_category("income")
                        elif selectedOption == "Add expense category":
                            self.add_category("expense")
                        elif selectedOption == "Main menu":
                            return "Main menu"
                        elif selectedOption == "Exit":
                            exit(self.startTime)
                    else:
                        raise ValueError("Number out of range")
                else:
                    raise ValueError("Invalid input")
            except ValueError as e:
                self.display_category_menu(str(e))
                # Pause to show the error message and then get input again if our input value was not valid.
                time.sleep(2)
            except Exception as e:
                Console.print(Text(f"An unexpected error occurred: {e}", style=red))
                return None
