import csv
import re
from datetime import datetime


class RegisterFine:
    def __init__(self, incomeFile="income.csv", costFile="cost.csv"):
        self.incomeFile = incomeFile
        self.costFile = costFile
        # This part must be imported from categories.csv. This part is for Mani.
        self.categories = ['Salary', 'Investment', 'Freelance', 'Gift']
        self.types = ['Cash', 'Check', 'Cryptocurrency']
