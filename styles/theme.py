import tkinter as tk
from tkinter import ttk

# Theme Variables
BACKGROUND_COLOR = '#2D2D2D'
PRIMARY_COLOR = '#4E4E4E'
SECONDARY_COLOR = '#2D2D2D'
TEXT_COLOR = '#EAEAEA'
BUTTON_HOVER = '#3A3A3A'

def set_global_styles(root):
    style = ttk.Style(root)

    style.configure('TButton', 
                    background=SECONDARY_COLOR, 
                    foreground=TEXT_COLOR, 
                    borderwidth=2, 
                    relief='flat', 
                    highlightthickness=0)
    
    style.map('TButton', background=[('active', BUTTON_HOVER)]),
    
    style.configure('TFrame', background=PRIMARY_COLOR)

    style.configure('TLabel', background=PRIMARY_COLOR, foreground=TEXT_COLOR)

    # Set default styles for Tk widgets
    root.option_add('*Background', '#2D2D2D')
    
    style.theme_use('default')