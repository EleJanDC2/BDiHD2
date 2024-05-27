import tkinter as tk
from tkinter import ttk

from styles.theme import PRIMARY_COLOR

class VerticalMenu(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs, background=PRIMARY_COLOR)
        self.create_widgets()

    def create_widgets(self):
        self.button_new = ttk.Button(self, text="New", command=self.new_file)
        self.button_new.pack(fill=tk.X, pady=2)

        self.button_open = ttk.Button(self, text="Open", command=self.open_file)
        self.button_open.pack(fill=tk.X, pady=2)

        self.button_exit = ttk.Button(self, text="Exit", command=self.quit_app)
        self.button_exit.pack(fill=tk.X, pady=2)

    def new_file(self):
        print("New file action")

    def open_file(self):
        print("Open file action")

    def quit_app(self):
        self.quit()