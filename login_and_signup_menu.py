from colors import blue,green
from rich.console import Console
from rich.text import Text
from signup import User

class FirstMenu():
    def __init__(self):
        self.menu_options=['sign up','log in']
    def show_menu(self):
        Console().clear()
        Console().print(Text('Welcome to the accounting managment app !',style=blue))
        Console().print(Text('please choose whether you want to sign up or log in by parsing using the arrow keys or typing the option you want'),style=green)
    def handle_input(self,input):
        pass

if __name__=='__main__':
    menu=FirstMenu()
    menu.show_menu()
    option=input()
    if option=='sign up':
        while True:
            userX=User()
            try:
                userX.get_first_name(input('first name: '))
                userX.get_last_name(input('last name: '))
                userX.get_code_meli(input('national id: '))
                userX.get_phone_number(input('mobile number: '))
                userX.get_username(input('user name: '))
                userX.get_password(input('password: '))
                userX.check_repeated_password(input('confirm password: '))
                userX.get_city(str(Console().input(f'[bold white] please choose the city from this list: [cyan] {userX.savedcities} \n :')))
                userX.get_email(input('email: '))
                userX.get_birth_date(input('birth date: (yyyy/mm/dd) '))
                userX.get_security_questions_answer(input('What is your favorite car brand? '))
                userX.save_csv()
                break
            except ValueError as error:
                print(error)


