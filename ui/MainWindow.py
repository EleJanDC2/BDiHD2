import tkinter as tk
from tkinter import ttk
from ui.components.menu import VerticalMenu
from styles.theme import set_global_styles
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

class MainWindow(Singleton):
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
        self.menu = VerticalMenu(self.left_frame, search_info_callback=self.print_search_info)
        self.menu.pack(fill=tk.Y, expand=True)
        

        self.conn = None
        cur = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.create_widgets()

    def create_widgets(self):
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

    def run(self):
        self.root.mainloop()

    def on_button_click(self):
        print("Button clicked!")

    def update_chart(self, airport):
        # Fetch data related to the selected airport
        # This is a placeholder, replace it with your actual data fetching logic
        data = self.fetch_data_for_airport(airport)

        # Clear the existing plot
        self.ax.clear()

        # Plot the new data
        self.ax.plot(data)

        # Redraw the canvas
        self.canvas.draw()

    def fetch_data_for_airport(self, airport):
        menu = VerticalMenu(self.root)  # or use self.left_frame
        query = f'SELECT AVG("delay_time [minutes]") as average_delay FROM flight_stats WHERE internal_airport_id = \'{airport}\''
        results = menu.execute_query(query)
        return results

    def print_search_info(self, search_term, start_date, departure_date, data_count):
        print(f"Search Term: {search_term}")
        print(f"Start Date: {start_date}")
        print(f"Departure Date: {departure_date}")
        print(f"Data Count: {data_count}")
        data = self.fetch_data_for_airport(search_term)
        print(data)

    def on_close(self):
        # Close the PostgreSQL connection here
        if self.conn is not None:
            self.conn.close()
        self.root.quit()
        self.root.destroy()
