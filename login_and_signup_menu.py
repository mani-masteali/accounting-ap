from colors import green,blue,cyan,red
from rich.console import Console
from rich.text import Text
from signup import User
from login import login_user,count_wrong_enters,forgot_password

class FirstMenu():
    def __init__(self):
        self.menu_options=['sign up','log in']
    def show_menu(self):
        Console().clear()
        Console().print(Text('Welcome to the accounting managment app !',style=blue))
        Console().print(Text('please choose your option 1 or 2'),style=green)
        Console().print(Text('1- sign up'),style=cyan)
        Console().print(Text('2- log in'),style=cyan)





