import csv
from datetime import datetime
from category import Category
from rich.console import Console
from rich.text import Text
import msvcrt
import time


class RegisterFine:
    def __init__(self, incomeFile="income.csv", expenseFile="expense.csv", incomeCategoryFile="incomeCategories.txt", expenseCategoryFile="expenseCategories.txt"):
        self.incomeFile = incomeFile
        self.expenseFile = expenseFile
        self.category = Category(incomeCategoryFile, expenseCategoryFile)
        self.incomeCategories = self.category.incomeCategories
        self.expenseCategories = self.category.expenseCategories
        self.types = ['Cash', 'Check', 'Cryptocurrency']
        self.selectedTypeIndex = 0
        self.selectedCategoryIndex = 0

    def registerIncome(self):
        if not self.incomeCategories:
            print("No income categories available. Please add categories first.")
            self.category.add_category("income")
            self.incomeCategories = self.category.incomeCategories

        amount = self.get_valid_input("Enter amount: ", self.is_amount_valid)
        date = self.get_valid_input(
            "Enter date in this format (mm/dd/yyyy): ", self.is_date_valid)
        category = self.select_category(self.incomeCategories, "income")
        description = self.get_valid_input(
            "Enter description (optional, 100 characters at most): ", self.is_description_valid, optional=True)
        type_ = self.select_type()

        record = [amount, date, category, description, type_]
        self.save_record(self.incomeFile, record)
        print("Income saved successfully.")

    def registerExpense(self):
        if not self.expenseCategories:
            print("No expense categories available. Please add categories first.")
            self.category.add_category("expense")
            self.expenseCategories = self.category.expenseCategories

        amount = self.get_valid_input("Enter amount: ", self.is_amount_valid)
        date = self.get_valid_input(
            "Enter date in this format (mm/dd/yyyy): ", self.is_date_valid)
        category = self.select_category(self.expenseCategories, "expense")
        description = self.get_valid_input(
            "Enter description (optional, 100 characters at most): ", self.is_description_valid, optional=True)
        type_ = self.select_type()

        record = [amount, date, category, description, type_]
        self.save_record(self.expenseFile, record)
        print("Expense saved successfully.")

    def get_valid_input(self, prompt, validation_func, optional=False):
        while True:
            user_input = input(prompt)
            if optional and user_input == '':
                return ''
            if validation_func(user_input):
                return user_input

    def is_amount_valid(self, amount):
        try:
            amount = float(amount)
            if amount > 0:
                return True
            else:
                print("Amount must be positive.")
                return False
        except ValueError:
            print("Amount must be a number.")
            return False

    def is_date_valid(self, date):
        try:
            datetime.strptime(date, '%m/%d/%Y')
            return True
        except ValueError:
            print("Date must be in the format mm/dd/yyyy.")
            return False

    def is_description_valid(self, description):
        if len(description) <= 100:
            return True
        else:
            print("Description must be 100 characters or less.")
            return False

    def save_record(self, file, record):
        with open(file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(record)

    def display_type_menu(self, errorMessage=None):
        console = Console()
        console.clear()
        console.print(Text("Select Type:", style="cyan"))
        console.print(
            Text("Use arrow keys to navigate and Enter to select.", style="gray"))
        if errorMessage:
            console.print(Text(f"Error: {errorMessage}", style="red"))
        for i, type_ in enumerate(self.types):
            if i == self.selectedTypeIndex:
                console.print(Text(f"-> {type_}", style="blue"))
            else:
                console.print(Text(f"   {type_}", style="cyan"))

    def handle_type_input(self):
        while True:
            self.display_type_menu()
            time.sleep(1) 
            key = msvcrt.getch()
            if key == b'\xe0':  # Arrow keys are preceded by '\xe0'
                keyCode = ord(msvcrt.getch())
                if keyCode == 72:  # Up arrow key
                    self.selectedTypeIndex = (
                        self.selectedTypeIndex - 1) % len(self.types)
                elif keyCode == 80:  # Down arrow key
                    self.selectedTypeIndex = (
                        self.selectedTypeIndex + 1) % len(self.types)
            elif key.isdigit():  # If a digit is pressed
                optionNum = int(key)
                if 1 <= optionNum <= len(self.types):
                    self.selectedTypeIndex = optionNum - 1
                    self.display_type_menu()  # Display menu again to update colors
                    time.sleep(1)
                    return self.types[self.selectedTypeIndex]

    def select_type(self):
        while True:
            selectedType = self.handle_type_input()
            if selectedType:
                return selectedType
            elif selectedType is None:
                print("Type selection canceled.")
                return ''

    def display_category_menu(self, categories, categoryType, errorMessage=None):
        console = Console()
        console.clear()
        console.print(
            Text(f"Select {categoryType.capitalize()} Category:", style="cyan"))
        console.print(Text(
            "Use arrow keys to navigate and Enter to select. Input the number of your choice.", style="gray"))
        if errorMessage:
            console.print(Text(f"Error: {errorMessage}", style="red"))
        for i, category in enumerate(categories):
            if i == self.selectedCategoryIndex:
                console.print(Text(f"-> {i+1}. {category}", style="blue"))
            else:
                console.print(Text(f"   {i+1}. {category}", style="cyan"))

    def handle_category_input(self, categories, categoryType):
        while True:
            self.display_category_menu(categories, categoryType)
            time.sleep(1)
            key = msvcrt.getch()
            if key == b'\xe0':  # Arrow keys are preceded by '\xe0'
                keyCode = ord(msvcrt.getch())
                if keyCode == 72:  # Up arrow key
                    self.selectedCategoryIndex = (
                        self.selectedCategoryIndex - 1) % len(categories)
                elif keyCode == 80:  # Down arrow key
                    self.selectedCategoryIndex = (
                        self.selectedCategoryIndex + 1) % len(categories)
            elif key.isdigit():  # If a digit is pressed
                optionNum = int(key)
                if 1 <= optionNum <= len(categories):
                    self.selectedCategoryIndex = optionNum - 1
                    # Display menu again to update colors
                    self.display_category_menu(categories, categoryType)
                    time.sleep(1)
                    return categories[self.selectedCategoryIndex]
            elif key == b'\r':  # Enter key
                return categories[self.selectedCategoryIndex]
            elif key == b'q':  # 'q' key
                return None

    def select_category(self, categories, categoryType):
        while True:
            selectedCategory = self.handle_category_input(
                categories, categoryType)
            if selectedCategory:
                return selectedCategory
            elif selectedCategory is None:
                print(f"{categoryType.capitalize()
                         } category selection canceled.")
