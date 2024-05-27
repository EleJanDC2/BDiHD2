import tkinter as tk
from tkinter import ttk

# Theme Variables
BACKGROUND_COLOR = '#2D2D2D'
PRIMARY_COLOR = '#4E4E4E'
SECONDARY_COLOR = '#2D2D2D'
TEXT_COLOR = '#EAEAEA'

def set_global_styles(root):
    style = ttk.Style(root)

    style.configure('TButton', 
                    background=SECONDARY_COLOR, 
                    foreground=TEXT_COLOR, 
                    borderwidth=0, 
                    relief='flat', 
                    highlightthickness=0)

    # Set default styles for Tk widgets
    root.option_add('*Background', '#2D2D2D')
    
    style.theme_use('default')