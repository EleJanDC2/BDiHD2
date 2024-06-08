from styles.theme import PRIMARY_COLOR, set_global_styles

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import psycopg2
from connection.config import load_config



class VerticalMenu(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs, background=PRIMARY_COLOR)
        self.create_widgets()
        set_global_styles(parent)

        # Set minimum width for the menu
        self.pack_propagate(0)
        self.config(width=300)


    def create_widgets(self):
        query = "SELECT DISTINCT internal_airport_id FROM flight_stats LIMIT 1000"
        results = self.execute_query(query)
        # Extract the airport codes from the results and assign them to list_to_search
        self.list_to_search = [result[0] for result in results]

        # Create a StringVar to hold the search term
        self.search_term = tk.StringVar()

        # Create an Entry widget for the search field
        self.search_field = ttk.Entry(self, textvariable=self.search_term)
        self.search_field.pack(fill=tk.X, pady=(0, 7.5))

        # Bind the KeyRelease event to the search function
        self.search_field.bind('<KeyRelease>', self.search_list)

        # Create a Listbox to display the search results
        self.search_results = tk.Listbox(self)

        # Insert the elements into the Listbox
        for element in self.list_to_search:
            self.search_results.insert(tk.END, element)

        self.search_results.pack(fill=tk.BOTH, expand=True, pady=7.5)

        # Create a Separator
        self.separator = ttk.Separator(self, orient='horizontal')
        self.separator.pack(fill=tk.X, pady=7.5)

        # Create a Label for the file actions
        self.file_label = ttk.Label(self, text="Arguments:")
        self.file_label.pack(fill=tk.X, pady=7.5)

        # Create a frame to group the widgets
        frame = ttk.Frame(self)

        # Create a label and date picker for start date
        start_date_label = ttk.Label(frame, text="Start Date:")
        start_date_label.grid(row=0, column=0, sticky=tk.E, padx=5, pady=7.5)
        self.start_date = DateEntry(frame)
        self.start_date.grid(row=0, column=1, sticky=tk.W, padx=5, pady=7.5)

        # Create a label and date picker for departure date
        departure_date_label = ttk.Label(frame, text="Departure Date:")
        departure_date_label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=7.5)
        self.departure_date = DateEntry(frame)
        self.departure_date.grid(row=1, column=1, sticky=tk.W, padx=5, pady=7.5)

        # Create a label and input for data count
        data_count_label = ttk.Label(frame, text="Data Count:")
        data_count_label.grid(row=2, column=0, sticky=tk.E, padx=5, pady=7.5)
        self.data_count = ttk.Entry(frame)
        self.data_count.grid(row=2, column=1, sticky=tk.W, padx=5, pady=7.5)

        # Add the frame to the parent widget
        frame.pack()

        # Create a Button to start search
        self.start_search_button = ttk.Button(self, text="Search", command=self.new_file)
        self.start_search_button.pack(fill=tk.X, pady=7.5)

        # Add the frame to the parent widget
        frame.pack()

    def search_list(self, event=None):
        # Clear the Listbox
        self.search_results.delete(0, tk.END)

        # Get the search term
        term = self.search_term.get()

        # Search the list
        results = [item for item in self.list_to_search if term in item]

        # Add the results to the Listbox
        for result in results:
            self.search_results.insert(tk.END, result)

    def new_file(self):
        query = "SELECT * FROM flight_stats LIMIT 1000 OFFSET 20"
        results = self.execute_query(query)
        print(results)

    def execute_query(self, query, args=None):
        try:
            # Load the configuration
            config = load_config()

            # Connect to the PostgreSQL server
            conn = psycopg2.connect(**config)

            # create a cursor
            cur = conn.cursor()
            
            # execute the query
            cur.execute(query, args)
            
            # fetch all the results
            results = cur.fetchall()
            
            # return the results
            return results
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
                print('Database connection closed.')

    def quit_app(self):
        self.quit()