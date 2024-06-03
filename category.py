import re


class Category:
    def __init__(self, file="categories.txt"):
        self.file = file
        self.categoriesList = self.load_categories(self)

    def load_categories(self):
        try:
            with open(self.file, mode='r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []

    def save_categories(self):
        with open(self.file, mode="w") as f:
            for cat in self.categoriesList:
                f.write(cat+"\n")

    def add_category(self):
        while True:
            category = input("Enter new category name: ")
            if self.is_category_valid(category):
                if category in self.categoriesList:
                    print(f"Category {category} already exists.")
                else:
                    self.categoriesList.append(category)
                    self.save_categories()
                    print(f"Category {category} added successfully.")
                break

    def is_category_vailid(self, category):
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
