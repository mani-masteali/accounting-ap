import re
import pandas
class Search:
    def __init__(self,searchedText):
        #allows the user to search their desired string
        self.searchedText=searchedText
        self.incomeFile=pandas.read_csv('income.csv')
        self.costsFile=pandas.read_csv('cost.csv')
        self.filters=[]
    #this allows us to print the filters
    def show_search_filters(self):
        print('if you want to choose filters, type the numbers seperated by spaces')
        print('1- incomes or costs of a special day')
        print('2- incomes or costs of a special month')
        print('3- incomes or costs of a special year')
        print('4- just incomes or costs')
        print('5- incomes or costs in a special range of financial price')
        print('6- search only in explanations or only in type of income or cost or only in source or a mix of them')
        self.filters=input('please enter your desired filters here: ').split()
    def day_income_or_cost(self):
        if '1' in self.filters:
            day=input('enter the day you want to check: (yyyy/mm/dd) ')
            if '4' not in self.filters:
                filtered_income = self.incomeFile.loc[self.incomeFile['date'].str.contains(day)]
                filtered_costs = self.costsFile.loc[self.costsFile['date'].str.contains(day)]
                return filtered_income, filtered_costs
            elif self.income_or_cost()==1:
                filtered_income = self.incomeFile.loc[self.incomeFile['date'].str.contains(day)]
                return filtered_income
            elif self.income_or_cost()==2:
                filtered_costs = self.costsFile.loc[self.costsFile['date'].str.contains(day)]
                return filtered_costs
    def month_income_or_cost(self):
        if '2' in self.filters:
            month=input('enter the month you want to check: (yyyy/mm) ')
            if '4' not in self.filters:
                filtered_income = self.incomeFile.loc[self.incomeFile['date'].str.contains(month)]
                filtered_costs = self.costsFile.loc[self.costsFile['date'].str.contains(month)]
                return filtered_income, filtered_costs
            elif self.income_or_cost()==1:
                filtered_income = self.incomeFile.loc[self.incomeFile['date'].str.contains(month)]
                return filtered_income
            elif self.income_or_cost()==2:
                filtered_costs = self.costsFile.loc[self.costsFile['date'].str.contains(month)]
                return filtered_costs
    def year_income_or_cost(self):
        if '3' in self.filters:
            year=input('enter the year you want to check: (yyyy) ')
            if '4' not in self.filters:
                filtered_income = self.incomeFile.loc[self.incomeFile['date'].str.contains(year)]
                filtered_costs = self.costsFile.loc[self.costsFile['date'].str.contains(year)]
                return filtered_income, filtered_costs
            elif self.income_or_cost()==1:
                filtered_income = self.incomeFile.loc[self.incomeFile['date'].str.contains(year)]
                return filtered_income
            elif self.income_or_cost()==2:
                filtered_costs = self.costsFile.loc[self.costsFile['date'].str.contains(year)]
                return filtered_costs
    def income_or_cost(self):
        if '4' in self.filters:
            income_or_cost=input('choose whether you want to see the incomes or costs ')
            if income_or_cost== 'income':
                return 1
            elif income_or_cost== 'cost':
                return 2
    def special_range(self):
        if '5' in self.filters:
            value_range=input('please enter your wanted range in this format: min-max')
            min,max=int(value_range.split('-'))
            return min,max
    def specify(self):
        if '6' in self.filters:
            wanted=input('please enter either the explantion you want or the type of income or outcome or the source of either one of them: (type of request: filter)')
            if '4' not in self.filters:
                    if 'explanation' in wanted:
                        filtered_income = self.incomeFile.loc[self.incomeFile['description'].str.contains(wanted)]
                        filtered_costs = self.costsFile.loc[self.costsFile['description'].str.contains(wanted)]
                        return filtered_income, filtered_costs
                    elif 'type' in wanted:
                        filtered_income = self.incomeFile.loc[self.incomeFile['type_'].str.contains(wanted)]
                        filtered_costs = self.costsFile.loc[self.costsFile['type_'].str.contains(wanted)]
                        return filtered_income, filtered_costs
                    elif 'source' in wanted:
                        filtered_income = self.incomeFile.loc[self.incomeFile['source'].str.contains(wanted)]
                        filtered_costs = self.costsFile.loc[self.costsFile['source'].str.contains(wanted)]
                        return filtered_income, filtered_costs
        elif self.income_or_cost()==1:
            if 'explanation' in wanted:
                filtered_income = self.incomeFile.loc[self.incomeFile['description'].str.contains(wanted)]
                return filtered_income
            elif 'type' in wanted:
                filtered_income = self.incomeFile.loc[self.incomeFile['type_'].str.contains(wanted)]
                return filtered_income
            elif 'source' in wanted:
                filtered_income = self.incomeFile.loc[self.incomeFile['source'].str.contains(wanted)]
                return filtered_income
            elif self.income_or_cost()==2:
                if 'explanation' in wanted:
                    filtered_costs = self.costsFile.loc[self.costsFile['description'].str.contains(wanted)]
                    return filtered_costs
                elif 'type' in wanted:
                    filtered_costs = self.costsFile.loc[self.costsFile['type_'].str.contains(wanted)]
                    return filtered_costs
                elif 'source' in wanted:
                    filtered_costs = self.costsFile.loc[self.costsFile['source'].str.contains(wanted)]
                    return filtered_costs