from colors import * 
from rich.console import Console
from rich.text import Text
import re
import pandas
# در اینجا اطلاعات مربوط به کاربر به صورت یک شی از کلاس یوزر ساخته و تعریف می شود
class User:
    def __init__(self):
        self.firstName=None
        self.lastName=None
        self.nationalId=None
        self.phoneNumber=None
        self.userName=None
        self.password=None
        self.city=None
        self.email=None
        self.birthDate=None
        self.securityQAnswer=None
        self.savedcities = [
            'Alborz',
            'Ardabil',
            'Bushehr',
            'Chaharmahal and Bakhtiari',
            'East Azerbaijan',
            'Fars',
            'Gilan',
            'Golestan',
            'Hamadan',
            'Hormozgan',
            'Ilam',
            'Isfahan',
            'Kerman',
            'Kermanshah',
            'Khuzestan',
            'Kohgiluyeh and Buyer Ahmad',
            'Kurdistan',
            'Lorestan',
            'Markazi',
            'Mazandaran',
            'North Khorasan',
            'Qazvin',
            'Qom',
            'Razavi Khorasan',
            'Semnan',
            'Sistan and Baluchestan',
            'South Khorasan',
            'Tehran',
            'West Azerbaijan',
            'Yazd',
            'Zanjan']            # بررسی معتبر بودن اسم کوچک و تعریف آن برای کاربر
    def get_first_name(self,firstName):
        if len(re.findall('[a-z]',firstName))+len(re.findall('[A-Z]',firstName)) == len(firstName):
            self.firstName=firstName
        else:
            raise ValueError(Console().print('[red]first name must only consist of English letters.'))
        return
    # بررسی معتبر بودن نام خانوادگی و تعریف آن برای کاربر
    def get_last_name(self,lastName):
        if len(re.findall('[a-z]',lastName))+len(re.findall('[A-Z]',lastName)) == len(lastName):
            self.lastName=lastName
        else:
            raise ValueError(Console().print('[red]last name must only consist of English letters.'))
        return
    #بررسی معتبر بودن کد ملی و تعریف آن برای کاربر
    def get_code_meli(self,nationalId):
        if len(nationalId)==10 :
            if len(re.findall('[0-9]',nationalId))==len(nationalId):
                self.nationalId=nationalId
            else:
                raise ValueError(Console().print('[red]National ID only has numbers in it.'))
        else:
            raise ValueError(Console().print('[red]National ID must have ten numbers.'))
        return 
    #بررسی معتبر بودن شماره تلفن و تعریف آن برای کاربر
    def get_phone_number(self,phoneNumber):
        if len(phoneNumber)==11 and len(re.findall('[0-9]',phoneNumber))==len(phoneNumber) and  bool(re.search('^09.',phoneNumber))==True:
            self.phoneNumber=phoneNumber
        elif len(phoneNumber)!=11:
            raise ValueError(Console().print('[red]phone number must have eleven digits.'))
        elif len(re.findall('[0-9]',phoneNumber))!=len(phoneNumber):
            raise ValueError(Console().print('[red]phone number must only consist of digits.'))
        elif bool(re.search('^09.',phoneNumber))==False:
            raise ValueError(Console().print('[red]phone number must begin with 09.'))
        return 
    #گرفتن یوزرنیم از کاربر  که می تواند به هر شکل دلخواه باشد.
    def get_username(self,userName):
        df=pandas.read_csv('users.csv')
        if userName not in df['userName'].values:
            self.userName=userName
        else:
            raise ValueError(Console().print('[red] this username already exits. try choosing a different one.'))
    #گرفتن پسورد در صورتی که شرایط دلخواه مسئله را رعایت کند
    def get_password(self,password):
        if len(password)>=6 and len(re.findall('[a-z]',password))>=1 and len(re.findall('[A-Z]',password))>=1 and len(re.findall("[!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]",password))>=1 and len(re.findall('[0-9]',password))>=1:
            self.password=password
        elif len(password)<6:
            raise ValueError(Console().print('[red]password must be at least 6 characters long.'))
        elif len(re.findall('[a-z]',password))<1:
            raise ValueError(Console().print('[red]password must contain at least one lowercase letter.'))
        elif len(re.findall('[A-Z]',password))<1:
            raise ValueError(Console().print('[red]password must contain at least one uppercase letter.'))
        elif len(re.findall("!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"),password)<1:
            raise ValueError(Console().print('[red]password must contain at least one digit.'))
        elif len(re.findall('[0-9]',password))<1:
            raise ValueError(Console().print('[red]password must contain at least one special character (!#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~).'))
        return
    #برای تایید رمز عبور  
    def check_repeated_password(self,repeatedPassword):
        if repeatedPassword!=self.password:
            Console.print('passwords do not match',style=red)
    # گرفتن نام شهر از کاربر در صورتی که در لیست تعریف شده باشد
    def get_city(self,city):
        if city in self.savedcities:
            self.city=city
        else:
            raise ValueError(Console().print(f'[red]Invalid city. Please choose the city from this list: [cyan]{self.savedcities}.'))
        return 
    # بررسی معتبر بودن ایمیل و گرفتن از کاربر
    def get_email(self,email):
        df=pandas.read_csv('users.csv')
        if email not in df['email'].values:
            if bool(re.findall(r'[A-Za-z0-9]+@(gmail|yahoo)\.com',email))==True:
                self.email=email
            else:
                raise ValueError(Console().print(f'[red]Invalid email'))
            return
        else:
            raise ValueError(Console().print('[red] this email already exits. try choosing a different one.'))
    def get_birth_date(self,birthDate):
        if bool(re.findall('[1-2][0-9][0-9][0-9]/[0-1][0-9]/[0-3][0-9]',birthDate))==True:
            year=birthDate[0:4]
            month=birthDate[5:7]
            day=birthDate[8:10]
            if int(year)>=1920 and int(year)<=2005 and 1<=int(month)<=12:
                max_days={1:31,2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
                if 1<=int(day)<=max_days[int(month)]:
                    self.birthDate=birthDate
                else:
                    raise ValueError(Console().print(f'[red] invalid day. this month has only {max_days[month]}'))
            elif int(year)<1920 or int(year)>2005:
                raise ValueError(Console().print(f'[red]birth year must be between 1920 and 2005'))
            elif int(month)<1 or int(month)>12:
                raise ValueError(Console().print(f'[red]month must be between 1 and 12'))
        else:
            raise ValueError(Console().print(f'[red] invalid birth date format'))
        return
    #گرفتن پاسخ سوال امنیتی که از کاربر پرسیده می شود
    def get_security_questions_answer(self,answer):
        self.securityQAnswer=answer
    #اطلاعات کاربر در یک فایل سی اس وی ذخیره می شود
    def save_csv(self):
        users=pandas.read_csv('users.csv')

        new_user={
            'firstName':[self.firstName],
            'lastName':[self.lastName],
            'nationalId':[self.nationalId],
            'phoneNumber':[self.phoneNumber],
            'userName':[self.userName],
            'password':[self.password],
            'city':[self.city],
            'email':[self.email],
            'birthDate':[self.birthDate],
            'SecurityQAnswer':[self.securityQAnswer]
        }
        new_user=pandas.DataFrame(new_user)
        users=pandas.concat([users,new_user])
        users.to_csv('users.csv',index=False)
        
    
