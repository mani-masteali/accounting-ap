import pandas
class Report:
    # report's logic is similar to search. so I decided to copy some functions
    # from it after my 12th commit on github
    def __init__(self):
        #allows the user to search their desired string
        self.incomeFile=pandas.read_csv('income.csv')
        self.costsFile=pandas.read_csv('expense.csv')
        self.choice=None
    def show_search_filters(self):
        print('choose one of these options')
        print('1- incomes or costs of a special day')
        print('2- incomes or costs of a special month')
        print('3- incomes or costs of a special year')
        print('4- incomes or costs among a special value range')
        print('5- incomes or costs of a special category')
        print('6- incomes or costs of a special money type in the last year')
        self.choice=input('please enter your desired filter here: ')
    def report_for_a_day(self):
        if self.choice=='1':
            income_or_cost_or_both=input('choose if you want to see the report for incomes or costs or both ')
            day=input('please choose the day you want: (yyyy/mm/dd) ')
            if income_or_cost_or_both=='both':
                income=self.incomeFile[self.incomeFile['date'].str.contains(day)]
                costs=self.costsFile[self.costsFile['date'].str.contains(day)]
                print(f'incomes of {day}:')
                print(income)
                print(f'costs of {day}:')
                print(costs)
            elif income_or_cost_or_both=='income':
                income=self.incomeFile[self.incomeFile['date'].str.contains(day)]
                print(f'incomes of {day}:')
                print(income)
            elif income_or_cost_or_both=='costs':
                costs=self.costsFile[self.costsFile['date'].str.contains(day)]
                print(f'costs of {day}:')
                print(costs)
            else:
                print('invalid input')
    def report_for_a_month(self):
        if self.choice=='2':
            income_or_cost_or_both=input('choose if you want to see the report for incomes or costs or both ')
            month=input('please choose the day you want: (yyyy/mm) ')
            if income_or_cost_or_both=='both':
                income=self.incomeFile[self.incomeFile['date'].str.contains(month)]
                costs=self.costsFile[self.costsFile['date'].str.contains(month)]
                print(f'incomes of {month}:')
                print(income)
                print(f'costs of {month}:')
                print(costs)
            elif income_or_cost_or_both=='income':
                income=self.incomeFile[self.incomeFile['date'].str.contains(month)]
                print(f'incomes of {month}:')
                print(income)
            elif income_or_cost_or_both=='costs':
                costs=self.costsFile[self.costsFile['date'].str.contains(month)]
                print(f'costs of {month}:')
                print(costs) 
            else:
                print('invalid input')
    def report_for_a_year(self):
        if self.choice=='3':
            income_or_cost_or_both=input('choose if you want to see the report for incomes or costs or both ')
            year=input('please choose the day you want: (yyyy) ')
            if income_or_cost_or_both=='both':
                income=self.incomeFile[self.incomeFile['date'].str.contains(year)]
                costs=self.costsFile[self.costsFile['date'].str.contains(year)]
                print(f'incomes of {year}:')
                print(income)
                print(f'costs of {year}:')
                print(costs)
            elif income_or_cost_or_both=='income':
                income=self.incomeFile[self.incomeFile['date'].str.contains(year)]
                print(f'incomes of {year}:')
                print(income)
            elif income_or_cost_or_both=='costs':
                costs=self.costsFile[self.costsFile['date'].str.contains(year)]
                print(f'costs of {year}:')
                print(costs) 
            else:
                print('invalid input')
    def report_for_a_value_range(self):
        if self.choice=='4':
            income_or_cost_or_both=input('choose if you want to see the report for incomes or costs or both ')
            value_range=input('please enter your wanted range in this format: min-max ').split(sep='-')
            min_value,max_value=int(value_range[0]),int(value_range[1])
            if income_or_cost_or_both=='both':
                income=self.incomeFile[(self.incomeFile['amount']>=min_value)&(self.incomeFile['amount']<=max_value)]
                costs=self.costsFile[(self.costsFile['amount']>=min_value)&(self.costsFile['amount']<=max_value)]
                print(f'incomes between {min} and {max}:')
                print(income)
                print(f'costs between {min} and {max}:')
                print(costs)
            elif income_or_cost_or_both=='income':
                income=self.incomeFile[(self.incomeFile['amount']>=min_value)&(self.incomeFile['amount']<=max_value)]
                print(f'incomes between {min} and {max}:')
                print(income)
            elif income_or_cost_or_both=='costs':
                costs=self.costsFile[(self.costsFile['amount']>=min_value)&(self.costsFile['amount']<=max_value)]
                print(f'costs between {min} and {max}:')
                print(costs)
            else:
                print('invalid error')
    def report_for_a_category(self):
        if self.choice=='5':
            category=input('please enter the category you want a report of: ')
            income=self.incomeFile[self.incomeFile['category']==category]
            costs=self.costsFile[self.costsFile['category']==category]
            print(f'incomes from {category}:')
            print(income)
            print(f'costs of {category}:')
            print(costs)
        elif self.choice=='6':
            typeof=input('please enter the type you want a report of: ')
            income=self.incomeFile[(self.incomeFile['type_'].str.contains(typeof)) & (self.incomeFile['date'].str.contains('2024'))]
            costs=self.costsFile[(self.costsFile['type_'].str.contains(typeof)) & (self.incomeFile['date'].str.contains('2024'))]
            print(f'incomes from {typeof}:')
            print(income)
            print(f'costs of {typeof}:')
            print(costs)
    def show_search_results(self):
        k=[self.report_for_a_day(),self.report_for_a_month(),self.report_for_a_year(),
            self.report_for_a_value_range(),self.report_for_a_category()]
        for result in k:
            if isinstance(result,pandas.DataFrame):
                print(result)