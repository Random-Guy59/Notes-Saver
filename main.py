'''Notes Saver implemented with tkinter in python'''

__author__ = 'Random Coder 59'
__version__ = '1.0.1'
__email__ = 'randomcoder59@gmail.com'

from gui import *

if __name__ == '__main__':
    win = tk.Tk()
    style = Style(win)
    style.theme_use('clam')
    LoginWindow(win).run()
    win.mainloop()