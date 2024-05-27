import tkinter as tk
from tkinter import ttk

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple UI")
        self.root.geometry("400x300")
        
        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self.root, text="Hello, Tkinter!")
        label.pack(pady=20)

        button = ttk.Button(self.root, text="Click Me", command=self.on_button_click)
        button.pack(pady=10)

    def on_button_click(self):
        print("Button clicked!")

    def run(self):
        self.root.mainloop()
