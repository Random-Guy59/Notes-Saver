'''Email Verification for Notes Saver'''

from smtplib import SMTP_SSL
from random import randint
from tkinter.messagebox import showerror, showinfo
from tkinter.simpledialog import askinteger

import os
from dotenv import load_dotenv

load_dotenv('variables.env')

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
APP_NAME = os.getenv('APP_NAME')

def send_verification_code(recipent: str) -> bool:
    '''Sends a verification code to recipent. Returns if verified'''

    code = randint(1000, 10000)
    server = SMTP_SSL('smtp.gmail.com', 465)
    server.login(EMAIL, PASSWORD)
    try:
        server.sendmail(
        EMAIL, recipent,
        f'Subject: Python\nYour verification code is {code}\nEnter this code to register your account at Notes Saver, If you did not register then ignore this email''')
    except:
        showerror('Invalid email')
    finally:
        server.quit()

    user_code = askinteger(APP_NAME, f'''Verification code sent at {recipent}, 
        Enter the verification code to register''')
    if user_code == code:
        showinfo(APP_NAME, 'Successfully registered')
        return True
    else:
        showerror(APP_NAME, 'Incorrect code, Verification Failed')
        return False