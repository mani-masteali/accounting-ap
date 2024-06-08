import pandas
class Search:
    def __init__(self):
        #allows the user to search their desired string
        self.searchedText=None
        try:
            self.incomeFile=pandas.read_csv('income.csv')
            self.costsFile=pandas.read_csv('expense.csv')
        except:
            print('one of the categories are empty')
        self.filters=[]
    #this allows us to print the filters
    def show_search_filters(self):
        print('if you want to choose filters, type the numbers seperated by spaces. keep empty if don not want any')
        print('1- incomes or costs of a special day')
        print('2- incomes or costs of a special month')
        print('3- incomes or costs of a special year')
        print('4- just incomes or costs')
        print('5- incomes or costs in a special range of financial price')
        print('6- search only in explanations or only in type of income or cost or only in source or a mix of them')
        self.filters=input('please enter your desired filters here: ').split()
        self.income_or_cost_val=self.income_or_cost()
    def day_income_or_cost(self):
        if '1' in self.filters:
            day=input('enter the day you want to check: (yyyy/mm/dd) ')
            if '4' not in self.filters:
                filtered_income = self.incomeFile.loc[self.incomeFile['date'].str.contains(day)]
                filtered_costs = self.costsFile.loc[(self.costsFile['date'].str.contains(day))]
                return (filtered_income,filtered_costs) if not filtered_income.empty and not filtered_costs.empty else 'no results found!'
            elif self.income_or_cost_val==1:
                filtered_income = self.incomeFile.loc[(self.incomeFile['date'].str.contains(day))]
                return filtered_income if not filtered_income.empty else 'no results found'
            elif self.income_or_cost_val==2:
                filtered_costs = self.costsFile.loc[self.costsFile['date'].str.contains(day)]
                return filtered_costs if not filtered_costs.empty else 'no results found'
    def month_income_or_cost(self):
        if '2' in self.filters:
            month=input('enter the month you want to check: (yyyy/mm) ')
            if '4' not in self.filters:
                filtered_income = self.incomeFile.loc[self.incomeFile['date'].str.contains(month)]
                filtered_costs = self.costsFile.loc[self.costsFile['date'].str.contains(month)]
                return (filtered_income,filtered_costs) if not filtered_income.empty and not filtered_costs.empty else 'no results found!'
            elif self.income_or_cost_val==1:
                filtered_income = self.incomeFile.loc[self.incomeFile['date'].str.contains(month)]
                return filtered_income if not filtered_income.empty else 'no results found'
            elif self.income_or_cost_val==2:
                filtered_costs = self.costsFile.loc[self.costsFile['date'].str.contains(month)]
                return filtered_costs if not filtered_costs.empty else 'no results found'
    def year_income_or_cost(self):
        if '3' in self.filters:
            year=input('enter the year you want to check: (yyyy) ')
            if '4' not in self.filters:
                filtered_income = self.incomeFile.loc[self.incomeFile['date'].str.contains(year)]
                filtered_costs = self.costsFile.loc[self.costsFile['date'].str.contains(year)]
                return (filtered_income,filtered_costs) if not filtered_income.empty and not filtered_costs.empty else 'no results found!'
            elif self.income_or_cost_val==1:
                filtered_income = self.incomeFile.loc[self.incomeFile['date'].str.contains(year)]
                return filtered_income if not filtered_income.empty else 'no results found'
            elif self.income_or_cost_val==2:
                filtered_costs = self.costsFile.loc[self.costsFile['date'].str.contains(year)]
                return filtered_costs if not filtered_costs.empty else 'no results found'
    def income_or_cost(self):
        if '4' in self.filters:
            income_or_cost=input('choose whether you want to see the incomes or costs ')
            if income_or_cost== 'income':
                return 1
            elif income_or_cost== 'cost':
                return 2
        else:
            return 0
    def special_range(self):
        if '5' in self.filters:
            value_range=input('please enter your wanted range in this format: min-max ').split(sep='-')
            min_value,max_value=int(value_range[0]),int(value_range[1])
            if '4' not in self.filters:
                filtered_income = self.incomeFile.loc[(self.incomeFile['amount']>=min_value) & (self.incomeFile['amount']<=max_value)]
                filtered_costs = self.costsFile.loc[(self.costsFile['amount']>=min_value) & (self.costsFile['amount']<=max_value)]
                return (filtered_income,filtered_costs) if not filtered_income.empty and not filtered_costs.empty else 'no results found!'
            elif self.income_or_cost_val==1:
                filtered_income = self.incomeFile.loc[(self.incomeFile['amount']>=min_value) & (self.incomeFile['amount']<=max_value)]
                return filtered_income if not filtered_income.empty else 'no results found'
            elif self.income_or_cost_val==2:
                filtered_costs = self.costsFile.loc[(self.costsFile['amount']>=min_value) & (self.costsFile['amount']<=max_value)]
                return filtered_costs if not filtered_costs.empty else 'no results found'
    def specify(self):
        if '6' in self.filters:
            wanted=input('please enter either the explantion you want or the type of income or outcome or the source of either one of them: (type of request: filter) ')
            if '4' not in self.filters:
                    if 'explanation' in wanted:
                        filtered_income = self.incomeFile.loc[self.incomeFile['description'].str.contains(wanted[13:])]
                        filtered_costs = self.costsFile.loc[self.costsFile['description'].str.contains(wanted[13:])]
                        return (filtered_income,filtered_costs) if not filtered_income.empty and not filtered_costs.empty else 'no results found!'
                    elif 'type' in wanted:
                        filtered_income = self.incomeFile.loc[self.incomeFile['type_'].str.contains(wanted[6:])]
                        filtered_costs = self.costsFile.loc[self.costsFile['type_'].str.contains(wanted[6:])]
                        return (filtered_income,filtered_costs) if not filtered_income.empty and not filtered_costs.empty else 'no results found!'
                    elif 'source' in wanted:
                        filtered_income = self.incomeFile.loc[self.incomeFile['category'].str.contains(wanted[8:])]
                        filtered_costs = self.costsFile.loc[self.costsFile['category'].str.contains(wanted[8:])]
                        return (filtered_income,filtered_costs) if not filtered_income.empty and not filtered_costs.empty else 'no results found!'
            elif self.income_or_cost_val==1:
                if 'explanation' in wanted:
                    filtered_income = self.incomeFile.loc[self.incomeFile['description'].str.contains(wanted[13:])]
                    return filtered_income if not filtered_income.empty else 'no results found'
                elif 'type' in wanted:
                    filtered_income = self.incomeFile.loc[self.incomeFile['type_'].str.contains(wanted[6:])]
                    return filtered_income if not filtered_income.empty else 'no results found'
                elif 'source' in wanted:
                    filtered_income = self.incomeFile.loc[self.incomeFile['category'].str.contains(wanted[8:])]
                    return filtered_income if not filtered_income.empty else 'no results found'
                elif self.income_or_cost_val==2:
                    if 'explanation' in wanted:
                        filtered_costs = self.costsFile.loc[self.costsFile['description'].str.contains(wanted[13:])]
                        return filtered_costs if not filtered_costs.empty else 'no results found'
                    elif 'type' in wanted:
                        filtered_costs = self.costsFile.loc[self.costsFile['type_'].str.contains(wanted[6:])]
                        return filtered_costs if not filtered_costs.empty else 'no results found'
                    elif 'source' in wanted:
                        filtered_costs = self.costsFile.loc[self.costsFile['category'].str.contains(wanted[8:])]
                        return filtered_costs if not filtered_costs.empty else 'no results found'
        else:
            return None
    def empty_filters(self):
        if '0' in self.filters:
            searchText=input('enter the text you want to find in your data: ')
            try:
                filtered_income = self.incomeFile.loc[
                    (self.incomeFile['description'].str.contains(searchText, case=False)) |
                    (self.incomeFile['date'].str.contains(searchText, case=False)) |
                    (self.incomeFile['category'].str.contains(searchText, case=False)) |
                    (self.incomeFile['type_'].str.contains(searchText, case=False))
                ]

                filtered_costs = self.costsFile.loc[
                    (self.costsFile['description'].str.contains(searchText, case=False)) |
                    (self.costsFile['date'].str.contains(searchText, case=False)) |
                    (self.costsFile['category'].str.contains(searchText, case=False)) |
                    (self.costsFile['type_'].str.contains(searchText, case=False))
                ]
            except:
                print('Invalid text')
            if  not filtered_income.empty and not filtered_costs.empty and filtered_income is not None and filtered_costs is not None:
                return (filtered_income,filtered_costs) 
            else:
                return 'no results found!'
    def print_if_none_empty(self,filtered_income,filtered_costs):
            if not filtered_income.empty:
                return filtered_income
            if not filtered_costs.empty:
                return filtered_costs
            elif filtered_costs.empty and filtered_income.empty:
                    return 'no results found!'
    def back_to_the_main_menu(self):
        option=input('type Main Menu to get back:\n')
        return option
    def show_search_results(self):
        k=[self.day_income_or_cost(),self.month_income_or_cost(),self.year_income_or_cost(),
        self.special_range(),self.specify(),self.empty_filters()]
        if '4' not in self.filters:
            results_income=[k[i][0] for i in range(len(k)) if k[i] is not None and isinstance(k[i][0],pandas.DataFrame)]
            results_costs=[k[i][1] for i in range(len(k)) if k[i] is not None and isinstance(k[i][1],pandas.DataFrame)]
            try:
                final_result_income=results_income[0]
                final_result_costs=results_costs[0]
            except:
                print('no results found!')
            for result in results_income[1:]:
                final_result_income=final_result_income.merge(result, how='inner')
            for result in results_costs[1:]:
                final_result_costs=final_result_costs.merge(result,how='inner')
            print('incomes: ')
            try:
                print(final_result_income)
                print('costs:')
                print(final_result_costs)
            except:
                pass
        elif self.income_or_cost_val==1:
            results_income=[k[i] for i in range(len(k)) if k[i] is not None and isinstance(k[i],pandas.DataFrame)]
            try:
                final_result_income=results_income[0]
            except:
                print('no results found!')
            for result in results_income[1:]:
                final_result_income=final_result_income.merge(result, how='inner')
            print('incomes',final_result_income)
        elif self.income_or_cost_val==2:
            results_costs=[k[i] for i in range(len(k)) if k[i] is not None and isinstance(k[i],pandas.DataFrame)]
            try:
                final_result_costs=results_costs[0]
            except:
                print('no results found!')
            for result in results_costs[1:]:
                final_result_costs=final_result_costs.merge(result,how='inner')
            print('costs',final_result_costs)