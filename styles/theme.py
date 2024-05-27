import tkinter as tk
from tkinter import ttk

def set_global_styles(root):
    style = ttk.Style(root)

    # Define styles for ttk widgets
    style.configure('TLabel', font=('Helvetica', 12))
    style.configure('TButton', font=('Helvetica', 10), background='red')
    style.map('TButton', background=[('active', 'red')])

    # Set default styles for Tk widgets
    root.option_add('*TButton*Background', 'lightgray')
    root.option_add('*TButton*Foreground', 'black')
    root.option_add('*Font', 'Helvetica 12')
    root.option_add('*Background', 'white')
    root.option_add('*Foreground', 'black')
    
    style.theme_use('default')