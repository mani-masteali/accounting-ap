import pandas
class Report:
    def __init__(self):
        #allows the user to search their desired string
        self.incomeFile=pandas.read_csv('income.csv')
        self.costsFile=pandas.read_csv('cost.csv')
        self.choice=None
    def show_search_filters(self):
        print('choose one of these options')
        print('1- incomes or costs of a special day')
        print('2- incomes or costs of a special month')
        print('3- incomes or costs of a special year')
        print('4- incomes or costs among a special value range')
        print('5- incomes or costs of a special category')
        print('6- incomes or costs of a special category in the last year')
        self.choice=input('please enter your desired filter here: ')
    def report_for_a_day(self):
        if self.choice==1:
            day=input('please choose the day you want: (yyyy/mm/dd)')
            income=self.incomeFile[self.incomeFile['date']==day]
            costs=self.costsFile[self.costsFile['date']==day]
            print(f'incomes of {day}:')
            print(income)
            print(f'costs of {day}:')
            print(costs)
    def report_for_a_month(self):
        if self.choice==2:
            month=input('please choose the month you want: (yyyy/mm)')
            income=self.incomeFile[self.incomeFile['date'].str.contains(month)]
            costs=self.costsFile[self.costsFile['date'].str.contains(month)]
            print(f'incomes of {month}:')
            print(income)
            print(f'costs of {month}:')
            print(costs)
    def report_for_a_year(self):
        if self.choice==3:
            year=input('please choose the year you want: (yyyy)')
            income=self.incomeFile[self.incomeFile['date'].str.contains(year)]
            costs=self.costsFile[self.costsFile['date'].str.contains(year)]
            print(f'incomes of {year}:')
            print(income)
            print(f'costs of {year}:')
            print(costs)
    def report_for_a_value_range(self):
        if self.choice==4:
            value_range=input('please enter your wanted range in this format: min-max')
            min,max=int(value_range.split(sep='-'))
            income=self.incomeFile[(self.incomeFile['amount']>=min)&(self.incomeFile['amount']<=max)]
            costs=self.costsFile[(self.costsFile['amount']>=min)&(self.costsFile['amount']<=max)]
            print(f'incomes between {min} and {max}:')
            print(income)
            print(f'costs between {min} and {max}:')
            print(costs)
    def report_for_a_category(self):
        if self.choice==5:
            category=input('please enter the category you wanted a report of: ')
            income=self.incomeFile[self.incomeFile['category']==category]
            costs=self.costsFile[self.costsFile['category']==category]
            print(f'incomes from {category}:')
            print(income)
            print(f'costs of {category}:')
            print(costs)
        elif self.choice==6:
            type=input('please enter the type you wanted a report of: ')
            income=self.incomeFile[self.incomeFile['type_']==type & self.incomeFile['date'].str.contains('2024')]
            costs=self.costsFile[self.costsFile['type_']==type & self.incomeFile['date'].str.contains('2024')]
            print(f'incomes from {type}:')
            print(income)
            print(f'costs of {type}:')
            print(costs)