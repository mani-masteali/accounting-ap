import re
import sys
import msvcrt
import time


class Category:
    def __init__(self, incomeFile="incomeCategories.txt", costFile="costCategories.txt"):
        self.incomeFile = incomeFile
        self.costFile = costFile
        self.incomeCategories = self.load_categories(self.incomeFile)
        self.costCategories = self.load_categories(self.costFile)
        self.categoriesMenuOptions = [
            "Add income category", "Add cost category", "Main menu", "Exit"]
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
            category = input(f"Enter new {categoryType} category name: ")
            if self.is_category_valid(category):
                if categoryType == "income":
                    if category in self.incomeCategories:
                        print(f"Income category '{category}' already exists.")
                    else:
                        self.incomeCategories.append(category)
                        self.save_categories(
                            self.incomeFile, self.incomeCategories)
                        print(f"Income category '{
                              category}' added successfully.")
                elif categoryType == "cost":
                    if category in self.costCategories:
                        print(f"Cost category '{category}' already exists.")
                    else:
                        self.costCategories.append(category)
                        self.save_categories(
                            self.costFile, self.costCategories)
                        print(f"Cost category '{
                              category}' added successfully.")
                break

    def is_category_valid(self, category):
        if not category:
            print("Category name cannot be empty.")
            return False
        if len(category) > 15:
            print("Category name must be 15 characters or less.")
            return False
        if not re.match("^[A-Za-z0-9]+$", category):
            print("Category name must contain only letters and numbers.")
            return False
        return True

    def show_categories(self,errorMessage=None):
        try:
            print("Income Categories:")
            for cat in self.incomeCategories:
                print(f"- {cat}")

            print("\nCost Categories:")
            for cat in self.costCategories:
                print(f"- {cat}")

            key = msvcrt.getch()
            if key == b'\xe0':  # Arrow keys are preceded by '\xe0'. if this conditon not checked, we will get an invalid input error when using arrow keys
                keyCode = ord(msvcrt.getch())
                if keyCode == 72:  # Up arrow key
                    self.categoriesMenuSelectedOption = (
                        self.categoriesMenuSelectedOption - 1) % len(self.categoriesMenuSelectedOption)
                elif keyCode == 80:  # Down arrow key
                    self.categoriesMenuSelectedOption = (
                        self.categoriesMenuSelectedOption + 1) % len(self.categoriesMenuSelectedOption)
            elif key == b'\r':  # Enter key
                time.sleep(1)
                return self.options[self.selectedOption]
            elif key == b'q':  # 'q' key
                self.exit()
            elif key.isdigit():  # If a digit is pressed
                optionNum = int(key)
                if 1 <= optionNum <= len(self.categoriesMenuOptions):
                    return self.categoriesMenuOptions[optionNum - 1]
                else:
                    raise ValueError("Number out of range")
            else:
                raise ValueError("Invalid input")
        except ValueError as e:
            self.show_categories(str(e))
            # Pause to show the error message and then get input again if our input value was not valid.
            time.sleep(3)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

        self.display_menu()

        choice = self.get_user_input()
        if choice == b'1':
            self.add_category("income")
        elif choice == b'2':
            self.add_category("cost")
        elif choice == b'3':
            self.show_main_menu()
        elif choice == b'4':
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

    def display_menu(self):
        while True:

            print("\nOptions:")
            print("1- Add Income Category")
            print("2- Add Cost Category")
            print("3- Main menu")
            print("4- Exit")
            print("Choose an option: ", end='', flush=True)

    def get_user_input(self):
        while True:
            key = msvcrt.getch()
            if key in [b'1', b'2', b'3', b'4']:
                return key
            elif key == b'\xe0':  # Arrow keys are preceded by '\xe0'. if this conditon not checked, we will get an invalid input error when using arrow keys
                next_key = msvcrt.getch()
                if next_key in [b'H', b'P']:  # Up, Down
                    print(next_key)
                else:
                    print("Invalid key. Please try again.")

    def show_main_menu(self):
        print("Returning to the main menu...")
        # This part must be completed


if __name__ == "__main__":
    category = Category()
    category.show_categories()
