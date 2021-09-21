'''Database related functions'''

import sqlite3
import bcrypt
from tkinter.messagebox import showerror
from encrypt_hash import encrypt_json

import os
from dotenv import load_dotenv

load_dotenv('variables.env')

APP_NAME = os.getenv('APP_NAME')
DATABASE = os.getenv('DATABASE')

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

def execute_query(query: str, args: tuple=()):
    '''Executes a query, commits it and returns the result of the query.'''

    result = cursor.execute(query, args)
    conn.commit()
    return result

execute_query('CREATE TABLE IF NOT EXISTS ACCOUNTS(EMAIL TEXT, PASSWORD TEXT, NOTES TEXT)')
'''
EMAIL             PASSWORD          NOTES
John@gmail.com    John's pw(hash)   '["Tab1", "Tab2"]'(encrypted)
'''

def get_all_accounts() -> dict:
    '''Returns a dict of all accounts with their passwords.
    For example: {'John@gmail.com': 'John's password'(hash), ...}'''

    accounts = execute_query('SELECT * FROM ACCOUNTS').fetchall()
    return {email: key for email, key, _ in accounts}

def get_account(email: str) -> tuple:
    '''Retuns account details of the email.
    For example: ('John@gmail.com': 'John's password'(hash), '["Tab1", "Tab2"]'(encrypted)'''

    return execute_query('SELECT * FROM ACCOUNTS WHERE EMAIL = ?', (email,)).fetchone()

def verify_login(email: str, key: str) -> bool:
    '''Checks if the email exist and key matches.'''

    accounts = get_all_accounts()
    if email in accounts.keys() and bcrypt.checkpw(key.encode(), accounts[email]):
        return True
    else:
        showerror(APP_NAME, 'Wrong credentials')
        return False

def verify_register(email: str, key: str) -> bool:
    '''Verifies if you can register using a email. Also checks the password requirement'''

    accounts = get_all_accounts()
    if email in accounts.keys():
        showerror(APP_NAME, 'The provided email has already been registered.')
    elif len(key) < 8:
        showerror(APP_NAME, 'Password should be atleast 8 charactars.')
    elif not key.isalnum():
        showerror(APP_NAME, 'Password should not contain non-alpahumeric charactars.')
    else:
        return True
    return False

def create_account(email: str, key: str) -> None:
    '''Creates a new account with the email and key and saves it in the database.'''

    hashed_key = bcrypt.hashpw(key.encode(), bcrypt.gensalt())
    encrypted_notes = encrypt_json([''])
    execute_query('INSERT INTO ACCOUNTS VALUES(?, ?, ?)', (email, hashed_key, encrypted_notes))