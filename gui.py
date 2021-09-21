'''GUI for Notes Saver'''

import tkinter as tk
from tkinter.ttk import Notebook, Style
from tkinter.messagebox import askyesno
from database_funcs import *
from encrypt_hash import *
from verification import *

import os
from dotenv import load_dotenv

load_dotenv('variables.env')

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
APP_NAME = os.getenv('APP_NAME')
DATABASE = os.getenv('DATABASE')
SECRET_FILE = os.getenv('SECRET_FILE')

class LoginWindow:
    '''Login Window class'''

    def __init__(self, win: tk.Tk) -> None:
        '''Initializing...'''

        self.win = win
        self.font = 'Arial 12'
        self.email_var = tk.StringVar(win)
        self.key_var = tk.StringVar(win)

    def run(self) -> None:
        '''Sets up the window'''

        for widget in self.win.winfo_children():
            widget.destroy()
        self.win.title(APP_NAME)
        self.win.geometry('250x175')
        self.win.resizable(False, False)
        self.build_layout()

    def get_details(self) -> None:
        '''Returns the email and key entered.'''

        return self.email_var.get().strip(), self.key_var.get().strip()

    def register(self) -> None:
        '''Registers the user'''

        email, key = self.get_details()
        if verify_register(email, key) and send_verification_code(email):
            create_account(email, key)
            NoteSaverWindow(self.win, get_account(email)).run()

    def login(self) -> None:
        '''Logs the user in'''

        email, key = self.get_details()
        if verify_login(email, key):
            NoteSaverWindow(self.win, get_account(email)).run()

    def build_layout(self) -> None:
        '''Builds the window layout'''

        for num in range(5):
            self.win.grid_rowconfigure(num, weight= 1)
        for num in range(2):
            self.win.grid_columnconfigure(num, weight= 1)

        tk.Label(self.win, text= 'Email Id:', font= self.font).grid(
            columnspan= 2, sticky= 'nwes', padx= 5, pady= 5)
        tk.Entry(self.win, textvariable= self.email_var, font= self.font).grid(
            columnspan= 2, sticky= 'nwes', padx= 5, pady= 5)
        tk.Label(self.win, text= 'Password:', font= self.font).grid(
            columnspan= 2, sticky= 'nwes', padx= 5, pady= 5)
        tk.Entry(self.win, textvariable= self.key_var, font= self.font).grid(
            columnspan= 2, sticky= 'nwes', padx= 5, pady= 5)
        tk.Button(self.win, text= 'Login', command= self.login, 
            font= self.font).grid(sticky= 'nwes', padx= 5, pady= 5)
        tk.Button(self.win, text= 'Register', command= self.register, 
            font= self.font).grid(row= 4, column= 1, sticky= 'nwes', 
                padx= 5, pady= 5)

class NoteSaverWindow:
    '''Note Saver Window class'''

    def __init__(self, win: tk.Tk, details: tuple) -> None:
        '''Intializing...'''

        self.email, self.key, self.notes = details
        self.notes = decrypt_json(self.notes)
        self.win = win
        self.tab_count = 1
        self.texts = []

    def run(self) -> None:
        '''Sets up the window'''

        for widget in self.win.winfo_children():
            widget.destroy()
        self.win.title(f"{self.email}'s Notes Saver")
        self.win.geometry('500x500')
        self.win.resizable(True, True)
        self.build_layout()

    def logout(self, event=None) -> None:
        '''Logs the user out'''

        LoginWindow(self.win).run()

    def add_tab(self, text_content='') -> None:
        '''Adds a new tab in the notebook'''

        text = self.build_text(self.notebook)    
        text.insert('1.0', text_content)  
        self.notebook.add(text, text=f'Tab{self.tab_count}')
        self.texts.append(text)
        self.tab_count += 1

    def delete_tab(self) -> None:
        '''Asks the user and deletes the tab'''
        for widget in self.notebook.winfo_children():
            current_tab = self.notebook.select()
            tab_name = self.notebook.tab(current_tab, 'text')
            if str(widget) == current_tab:
                if askyesno(APP_NAME, f'Do you want to delete {tab_name}?'):
                    widget.destroy()
                    self.tab_count -= 1
                break

    def build_text(self, parent) -> None:
        '''Builds a new text widget'''

        text = tk.Text(parent)
        text.pack(expand=True, fill='both')
        scroll_bar = tk.Scrollbar(text)
        scroll_bar.pack(side='right', fill='y')
        scroll_bar.config(command=text.yview) 
        text.config(yscrollcommand=scroll_bar.set)
        return text

    def save_notes(self, event=None):
        '''Saves all the notes'''

        self.notes.clear()
        for text in self.texts:
            try:
                self.notes.append(text.get(1.0, 'end'))
            except:
                pass

        encrypted_notes = encrypt_json(self.notes)
        execute_query('UPDATE ACCOUNTS SET NOTES = ? WHERE EMAIL = ?', (encrypted_notes, self.email))

    def build_layout(self):
        for num in range(5):
            self.win.grid_rowconfigure(num, weight=0)
        for num in range(2):
            self.win.grid_columnconfigure(num, weight=0)

        main_menu = tk.Menu(self.win)
        self.win['menu'] = main_menu

        file_menu = tk.Menu(main_menu, tearoff=0) 
        main_menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Save', command=self.save_notes)
        file_menu.add_separator()
        file_menu.add_command(label='Logout', command=lambda: LoginWindow(self.win).run())
        file_menu.add_command(label='Exit', command=quit)

        edit_menu = tk.Menu(main_menu, tearoff= 0)
        main_menu.add_cascade(label='Edit', menu=edit_menu) 
        edit_menu.add_command(label='Add New Tab', command=self.add_tab)
        edit_menu.add_command(label='Delete Tab', command=self.delete_tab)

        self.notebook = Notebook(self.win)
        self.notebook.pack(expand=True, fill='both')
        for note in self.notes:
            self.add_tab(note)