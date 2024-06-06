from colors import green,blue,cyan,red
from rich.console import Console
from rich.text import Text
from signup import User
import getpass
from login import login_user,count_wrong_enters,forgot_password

class FirstMenu():
    def __init__(self):
        self.menu_options=['sign up','log in']
    def show_menu(self):
        Console().clear()
        Console().print(Text('Welcome to the accounting managment app !',style=blue))
        Console().print(Text('please choose whether your option'),style=green)
        Console().print(Text('1- sign up'),style=cyan)
        Console().print(Text('2- log in'),style=cyan)

if __name__=='__main__':
    menu=FirstMenu()
    menu.show_menu()
    option=input()
    if option=='1':
        while True:
            userX=User()
            try:
                userX.get_first_name(input('first name: '))
                userX.get_last_name(input('last name: '))
                userX.get_code_meli(input('national id: '))
                userX.get_phone_number(input('mobile number: '))
                userX.get_username(input('user name: '))
                userX.get_password(getpass.getpass('enter password:'))
                userX.check_repeated_password(getpass.getpass('confrim password:'))
                userX.get_city(str(Console().input(f'[bold white] please choose the city from this list: [cyan] {userX.savedcities} \n :')))
                userX.get_email(input('email: '))
                userX.get_birth_date(input('birth date: (yyyy/mm/dd) '))
                userX.get_security_questions_answer(input('What is your favorite car brand? '))
                userX.save_csv()
                last_option=str(Console().input('[green] type submit to continue\n'))
                if last_option=='submit':
                    break
                else:
                    Console().print('[bold red] Invalid input')
            except ValueError as error:
                print(error)
    elif option=='2':
        count=0
        while True:
            userName=input('username: ')
            password=getpass.getpass('password: ')
            if login_user(userName,password)==True:
                Console().print(Text('login was succesful!'),style=green)
                break
            else:
                Console().print(Text('username or password is wrong or does not exist!'),style=red)
                count+=1
                count_wrong_enters(count)
                forgotOrNot=input('forgot your password? ')
                if forgotOrNot=='Yes' or forgotOrNot=='yes':
                    userNameOrEmail=input('enter your username or email: ')
                    securityQAnswer=input('What is your favorite car brand? ')
                    forgot_password(userNameOrEmail,securityQAnswer)



