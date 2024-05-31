from colors import blue,green
from rich.console import Console
from rich.text import Text
from signup import *

class FirstMenu():
    def __init__(self):
        self.menu_options=['sign up','log in']
    def show_menu(self):
        Console.clear()
        Console.print(Text('Welcome to the accounting managment app !',style=blue))
        Console.print(Text('please choose whether you want to sign up or log in by parsing using the arrow keys or typing the option you want'),style=green)
    def handle_input(self,input):
        if 

if __name__=='__main__':
    firstMenu=FirstMenu.show_menu()


