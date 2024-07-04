from rich.console import Console
from rich.text import Text
import time
import pandas
from colors import green,red

def login_user(userName, passWord):
    users = pandas.read_csv('users.csv')
    for _, user in users.iterrows():
        if user['userName'] == userName and user['password'] == passWord:
            return True
    return False
def count_wrong_enters(count):
    if count%3==0:
        Console().print(Text('try again in one minute!'),style=red)
        time.sleep(60)
    else:
        pass
def forgot_password(userNameOrEmail,securityQAnswer):
    users = pandas.read_csv('users.csv')
    users['userName'] = users['userName'].astype(str).str.lower()
    users['email'] = users['email'].astype(str).str.lower()
    matching_users = users[
        (users['userName'] == userNameOrEmail.lower()) |
        (users['email'] == userNameOrEmail.lower())
    ]
    if not matching_users.empty:
        user = matching_users.iloc[0]  
        if user['SecurityQAnswer'] == securityQAnswer:
            Console().print(Text(f"Your password is: {user['password']}"), style=green)
        else:
            Console().print(Text("Security question answer is wrong!"), style=red)
    else:
        Console().print(Text("Username or email does not exist!"), style=red)


