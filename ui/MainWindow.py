import tkinter as tk
from tkinter import ttk
from ui.components.menu import VerticalMenu
from styles.theme import set_global_styles
import matplotlib
matplotlib.use('TkAgg')  # Set the backend to TkAgg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

class MainWindow(Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

        # Initialize the vertical menu with both callbacks
        self.menu = VerticalMenu(self.left_frame, search_info_callback=self.print_search_info, update_chart_callback=self.update_chart)
        self.menu.pack(fill=tk.Y, expand=True)
        
        self.conn = None
        cur = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.plot_lines = None
        self.create_widgets()

    def create_widgets(self):

        # Create a figure and axis for the chart
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_chart(self, data, x_label, y_label, title):
        if data is None:
            # Handle the case where data is None, perhaps log a warning or silently return
            return

        # Assuming data is a tuple or list of (x, y) values
        x_data, y_data = zip(*data)

        # Clear the previous plot
        self.ax.clear()

        # Create a bar chart
        self.ax.bar(x_data, y_data)

        # Optionally, you can set labels and title again if they get cleared with ax.clear()
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_title(title)
        # Redraw the canvas
        self.canvas.draw()


    def run(self):
        self.root.mainloop()

    def on_button_click(self):
        print("Button clicked!")

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
