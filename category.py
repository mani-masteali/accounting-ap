import re

import os


class Category:
    def __init__(self, incomeFile="incomeCategories.txt", costFile="costCategories.txt"):
        self.incomeFile = incomeFile
        self.costFile = costFile
        self.incomeCategories = self.load_categories(self.incomeFile)
        self.costCategories = self.load_categories(self.costFile)

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

    def show_categories(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Income Categories:")
            for cat in self.incomeCategories:
                print(f"- {cat}")

            print("\nCost Categories:")
            for cat in self.costCategories:
                print(f"- {cat}")

            print("\nOptions:")
            print("1- Add Income Category")
            print("2- Add Cost Category")
            print("3- Main menu")
            print("4- Exit")

            choice = input("Choose an option: ")
            if choice == "1":
                self.add_category("income")
            elif choice == "2":
                self.add_category("cost")
            elif choice == "3":
                os.system('cls' if os.name == 'nt' else 'clear')

            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    category = Category()

    # Show the categories and display the menu
    category.show_categories()
