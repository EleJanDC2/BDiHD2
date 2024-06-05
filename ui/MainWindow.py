import tkinter as tk
from tkinter import ttk
from ui.components.menu import VerticalMenu
from styles.theme import set_global_styles
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple UI")
        self.root.geometry("800x600")

        # Apply global styles
        set_global_styles(self.root)

        # Create the main layout frames
        self.left_frame = tk.Frame(self.root, width=200)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Initialize the vertical menu
        self.menu = VerticalMenu(self.left_frame)
        self.menu.pack(fill=tk.Y, expand=True)

        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self.right_frame, text="Hello, Tkinter!")
        label.pack(pady=20)

        button = ttk.Button(self.right_frame, text="Click Me", command=self.on_button_click)
        button.pack(pady=10)

        # Create a new figure and a subplot
        fig, ax = plt.subplots()

        # Create some example data
        x = [1, 2, 3, 4, 5]
        y = [1, 4, 9, 16, 25]

        # Plot the data
        ax.plot(x, y)

        # Create a canvas and add it to the frame
        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def on_button_click(self):
        print("Button clicked!")

    def run(self):
        self.root.mainloop()