import csv
import re
from datetime import datetime


class RegisterFine:
    def __init__(self, incomeFile="income.csv", costFile="cost.csv"):
        self.incomeFile = incomeFile
        self.costFile = costFile
        # This part must be imported from categories.csv. This part is for Mani not me.
        self.categories = ['Salary', 'Investment', 'Freelance', 'Gift']
        self.types = ['Cash', 'Check', 'Cryptocurrency']

    def registerIncome(self):
        amount = self.input("Enter amount :")
        date = self.input("Enter date in this format(dd/mm/yyyy) :")
        # it must be chosen from categories.csv. This part is for Mani not me.
        category = self.input("Enter category :")
        description = self.input(
            "Enter description (optional, 100 characters at last): ")
        type_ = self.input(f"Enter type ({', '.join(self.types)}): ")
        if self.is_amount_valid(amount) and self.is_date_valid(date) and self.is_category_valid(category) and self.is_type_valid(type_) and self.is_description_valid(description):
            record = [amount, date, category, description, type_]
            self.save_record(self.costFile, record)
            print("Income saved successfully.")
        else:
            print("Failed to save income due to invalid input.")

    def registerCost(self):
        amount = self.input("Enter amount :")
        date = self.input("Enter date in this format(mm/dd/yyyy) :")
        # it must be chosen from categories.csv. This part is for Mani not me.
        category = self.input("Enter category :")
        description = self.input(
            "Enter description (optional, 100 characters at last): ")
        type_ = self.input(f"Enter type ({', '.join(self.types)}): ")
        if self.is_amount_valid(amount) and self.is_date_valid(date) and self.is_category_valid(category) and self.is_type_valid(type_) and self.is_description_valid(description):
            record = [amount, date, category, description, type_]
            self.save_record(self.costFile, record)
            print("Cost saved successfully.")
        else:
            print("Failed to save cost due to invalid input.")
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

    def is_category_valid(self, category):
        # it must be checked that its in categoried.csv file or not. This part is for Mani not me.
        if category in self.categories:
            return True
        else:
            print("Invalid category. Choose from: " + ", ".join(self.categories))
            return False

    def is_type_valid(self, type_):
        if type_ in self.types:
            return True
        else:
            print("Invalid type. Choose from: " + ", ".join(self.types))
            return False
    def is_description_valid(self,description):
        if len(description) <= 100:
            return True
        else:
            print("Description must be 100 characters or less.")
            return False
    def save(self, file, record):
        with open(file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(record)
