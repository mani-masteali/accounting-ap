import csv
from datetime import datetime
from category import Category


class RegisterFine:
    def __init__(self, incomeFile="income.csv", costFile="cost.csv", incomeCategoryFile="incomeCategories.txt", costCategoryFile="costCategories.txt"):
        self.incomeFile = incomeFile
        self.costFile = costFile
        self.category = Category(incomeCategoryFile, costCategoryFile)
        self.incomeCategories = self.category.incomeCategories
        self.costCategories = self.category.costCategories
        self.types = ['Cash', 'Check', 'Cryptocurrency']

    def registerIncome(self):
        if not self.incomeCategories:
            print("No income categories available. Please add categories first.")
            self.category.add_category("income")
            self.incomeCategories = self.category.incomeCategories

        amount = self.get_valid_input("Enter amount: ", self.is_amount_valid)
        date = self.get_valid_input(
            "Enter date in this format (mm/dd/yyyy): ", self.is_date_valid)
        category = self.get_valid_input(
            "Enter income category: ", lambda x: self.is_category_valid(x, self.incomeCategories))
        description = self.get_valid_input(
            "Enter description (optional, 100 characters at most): ", self.is_description_valid, optional=True)
        type_ = self.get_valid_input(
            f"Enter type ({', '.join(self.types)}): ", self.is_type_valid)

        record = [amount, date, category, description, type_]
        self.save_record(self.incomeFile, record)
        print("Income saved successfully.")

    def registerCost(self):
        if not self.costCategories:
            print("No cost categories available. Please add categories first.")
            self.category.add_category("cost")
            self.costCategories = self.category_manager.costCategories

        amount = self.get_valid_input("Enter amount: ", self.is_amount_valid)
        date = self.get_valid_input(
            "Enter date in this format (mm/dd/yyyy): ", self.is_date_valid)
        category = self.get_valid_input(
            "Enter cost category: ", lambda x: self.is_category_valid(x, self.costCategories))
        description = self.get_valid_input(
            "Enter description (optional, 100 characters at most): ", self.is_description_valid, optional=True)
        type_ = self.get_valid_input(
            f"Enter type ({', '.join(self.types)}): ", self.is_type_valid)

        record = [amount, date, category, description, type_]
        self.save_record(self.costFile, record)
        print("Cost saved successfully.")

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

    def is_category_valid(self, category, categories):
        if category in categories:
            return True
        else:
            print(f"Invalid category. Choose from: {', '.join(categories)}")
            return False

    def is_type_valid(self, type_):
        if type_ in self.types:
            return True
        else:
            print(f"Invalid type. Choose from: {', '.join(self.types)}")
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


if __name__ == "__main__":
    financial_record = RegisterFine()
