from colors import *
from rich.console import Console
from rich.text import Text
import re
# در اینجا اطلاعات مربوط به کاربر به صورت یک شی از کلاس یوزر ساخته و تعریف می شود
class User:
    def __init__(self):
        self.firstName=None
        self.lastName=None
        self.nationalId=None
        self.phoneNumber=None
        self.userName=None
        self.password=None
        self.repeatedPassWord=None
        self.city=None
        self.email=None
        self.birthDate=None
        self.securityQAnswer=None
    # بررسی معتبر بودن اسم کوچک و تعریف آن برای کاربر
    def get_first_name(self,firstName):
        if len(re.findall('[a-z]',firstName))+len(re.findall('[A-Z]',firstName)) == len(firstName):
            self.firstName=firstName
        else:
            raise ValueError(Console.print('first name must only consist of english letters'),style=red)
    # بررسی معتبر بودن نام خانوادگی و تعریف آن برای کاربر
    def get_last_name(self,lastName):
        if len(re.findall('[a-z]',lastName))+len(re.findall('[A-Z]',lastName)) == len(lastName):
            self.lastName=lastName
        else:
            raise ValueError(Console.print('last name must only consist of english letters'),style=red)
    #بررسی معتبر بودن کد ملی و تعریف آن برای کاربر
    def get_code_meli(self,nationalId):
        if len(nationalId)==10 :
            if len(re.findall('[0-9]',nationalId))==len(nationalId):
                self.nationalId=nationalId
            else:
                Console.print('National ID only has numbers in it',style=red)
        else:
            raise ValueError(Console.print('National ID must have ten numbers',style=red))
    #بررسی معتبر بودن شماره تلفن و تعریف آن برای کاربر
    def get_phone_number(self,phoneNumber):
        if len(phoneNumber)==11 and len(re.findall('[0-9]',phoneNumber))==len(phoneNumber) and  bool(re.search('^09.',phoneNumber))==True:
            self.phoneNumber=phoneNumber
        elif len(phoneNumber)!=11:
            Console.print('phone number must have eleven digits',style=red)
        elif len(re.findall('[0-9]',phoneNumber))!=len(phoneNumber):
            Console.print('phone number must only consist of digits',style=red)
        elif bool(re.search('^09.',phoneNumber))==False:
            Console.print('phone number must begin with 09',style=red)
    #گرفتن یوزرنیم از کاربر  که می تواند به هر شکل دلخواه باشد.
    def get_username(self,userName):
        self.userName=userName

    