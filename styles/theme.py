import tkinter as tk
from tkinter import ttk

# Theme Variables
BACKGROUND_COLOR = '#2D2D2D'
PRIMARY_COLOR = '#4E4E4E'
SECONDARY_COLOR = '#2D2D2D'
TEXT_COLOR = '#EAEAEA'

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
    root.option_add('*Background', '#2D2D2D')  # Changed from 'white' to '#4E4E4E'
    root.option_add('*Foreground', 'black')
    
    style.theme_use('default')