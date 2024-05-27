import tkinter as tk
from tkinter import ttk

from styles.theme import PRIMARY_COLOR, set_global_styles


class VerticalMenu(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs, background=PRIMARY_COLOR)
        self.create_widgets()
        set_global_styles(parent)

        # Set minimum width for the menu
        self.pack_propagate(0)
        self.config(width=300)


    def create_widgets(self):
        # Create a list to search from
        self.list_to_search = ['item1', 'item2', 'item3', 'item4', 'item5']

        # Create a StringVar to hold the search term
        self.search_term = tk.StringVar()

        # Create an Entry widget for the search field
        self.search_field = ttk.Entry(self, textvariable=self.search_term)
        self.search_field.pack(fill=tk.X, pady=(0, 7.5))

        # Bind the KeyRelease event to the search function
        self.search_field.bind('<KeyRelease>', self.search_list)

        # Create a Listbox to display the search results
        self.search_results = tk.Listbox(self)
        self.search_results.pack(fill=tk.BOTH, expand=True, pady=7.5)

        # Create a Separator
        self.separator = ttk.Separator(self, orient='horizontal')
        self.separator.pack(fill=tk.X, pady=7.5)

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
        print("New file action")

    def open_file(self):
        print("Open file action")

    def quit_app(self):
        self.quit()