import tkinter as tk
from tkinter import ttk

# Theme Variables
BACKGROUND_COLOR = '#2D2D2D'
PRIMARY_COLOR = '#4E4E4E'
SECONDARY_COLOR = '#2D2D2D'
TEXT_COLOR = '#EAEAEA'
BUTTON_HOVER = '#3A3A3A'
FONT_SIZE = 12

def set_global_styles(root):
    style = ttk.Style(root)

    #style.configure('.', font=('Arial', FONT_SIZE))

    style.configure('TButton', 
                    background=SECONDARY_COLOR, 
                    foreground=TEXT_COLOR, 
                    borderwidth=2, 
                    relief='flat', 
                    highlightthickness=0)
    
    style.map('TButton', background=[('active', BUTTON_HOVER)]),
    
    style.configure('TFrame', background=PRIMARY_COLOR)

    style.configure('TLabel', background=SECONDARY_COLOR, foreground=TEXT_COLOR)

    style.configure('TEntry', fieldbackground=SECONDARY_COLOR, foreground=TEXT_COLOR, font=('Arial', FONT_SIZE))

    style.configure('TListbox', background=PRIMARY_COLOR, foreground=TEXT_COLOR, font=('Arial', FONT_SIZE))

    # Set default styles for Tk widgets
    root.option_add('*Background', '#2D2D2D')
    root.option_add('*Listbox.foreground', TEXT_COLOR)
    root.option_add('*Listbox.selectForeground', TEXT_COLOR)
    root.option_add('*Listbox.activestyle', 'none')
    
    style.theme_use('default')