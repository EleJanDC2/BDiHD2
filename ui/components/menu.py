from styles.theme import PRIMARY_COLOR, set_global_styles

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import psycopg2
from connection.config import load_config
import csv
from chartFun import *


class VerticalMenu(tk.Frame):
    def __init__(self, parent, search_info_callback=None, update_chart_callback=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs, background=PRIMARY_COLOR)
        self.search_info_callback = search_info_callback
        self.update_chart_callback = update_chart_callback  # Ensure this is assigned

        self.create_widgets()
        set_global_styles(parent)
        # Set minimum width for the menu
        self.pack_propagate(0)
        # Set the current button set to 1
        self.current_set = 1
        self.config(width=300)
        if self.current_set == 1:
            self.button_set_2.pack_forget()  # Ensure button_set_2 is not visible initially
        else:
            self.button_set_1.pack_forget()

    def update_chart(self, data, chart_title='Your Chart Title', x_axis_label='Your X-axis Label', y_axis_label='Your Y-axis Label'):
        if data is None:
            # Handle the case where data is None
            return

        x_data, y_data = zip(*data)

        self.ax.clear()
        self.ax.bar(x_data, y_data)
        self.ax.set_ylabel(y_axis_label)
        self.ax.set_xlabel(x_axis_label)
        self.ax.set_title(chart_title)

        self.canvas.draw()

    def create_widgets(self):
        query = "SELECT DISTINCT internal_airport_id FROM flight_stats LIMIT 1000"
        results = self.execute_query(query)
        self.list_to_search = [result[0] for result in results]
        self.search_term = tk.StringVar()
        self.search_field = ttk.Entry(self, textvariable=self.search_term)
        self.search_field.pack(fill=tk.X, pady=(0, 7.5))
        self.search_field.bind('<KeyRelease>', self.search_list)
        # Create the Listbox before trying to bind an event to it
        self.search_results = tk.Listbox(self)
        for element in self.list_to_search:
            self.search_results.insert(tk.END, element)
        self.search_results.pack(fill=tk.BOTH, expand=True, pady=7.5)
        # Now bind the event after the Listbox has been created
        self.search_results.bind('<<ListboxSelect>>', self.on_select)

        self.switch_button = ttk.Button(self, text="Switch Button Set", command=self.switch_button_set)
        self.switch_button.pack(fill=tk.X, pady=7.5)

        # Container for the first set of buttons
        self.button_set_1 = tk.Frame(self)
        ttk.Button(self.button_set_1, text="Average Arival Delay Time", command=self.chartButton1).pack(fill=tk.X, pady=7.5)
        ttk.Button(self.button_set_1, text="Average Departure Delay Time", command=self.chartButton2).pack(fill=tk.X, pady=7.5)
        ttk.Button(self.button_set_1, text="Flights per month", command=self.chartButton4).pack(fill=tk.X, pady=7.5)
        ttk.Button(self.button_set_1, text="Amount of Flights per Airport", command=self.chartButton5).pack(fill=tk.X, pady=7.5)
        ttk.Button(self.button_set_1, text="Amount of Arrivals per Airport", command=self.chartButton6).pack(fill=tk.X, pady=7.5)
        ttk.Button(self.button_set_1, text="Amount of Departures per Airport", command=self.chartButton7).pack(fill=tk.X, pady=7.5)
        self.button_set_1.pack(fill=tk.X, pady=7.5)

        # Container for the second set of buttons
        self.button_set_2 = tk.Frame(self)
        self.airport_code_label = ttk.Label(self.button_set_2, text="Airport code: ")
        self.airport_code_label.pack(fill=tk.X, pady=7.5)

        self.flights_amount_label = ttk.Label(self.button_set_2, text="Amount of flights: ")
        self.flights_amount_label.pack(fill=tk.X, pady=7.5)
        
        self.mean_ammount_of_for_month_flights = ttk.Label(self.button_set_2, text="Mean amount of flights per month: ")
        self.mean_ammount_of_for_month_flights.pack(fill=tk.X, pady=7.5)

        self.mean_delay_label = ttk.Label(self.button_set_2, text="Mean delay time: ")
        self.mean_delay_label.pack(fill=tk.X, pady=7.5)
        
        self.button_set_2.pack(fill=tk.X, pady=7.5)

    def on_select(self, event):
        # Get the index of the selected item
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            airport_code = event.widget.get(index)
            query = "SELECT * FROM flight_stats LIMIT 1000"
            results = self.execute_query(query)
            # Assuming generateBasicDataForAiport is defined in chartFun.py and imported
            data = generateBasicDataForAiport(airport_code, results)
            
            # Update the labels with the new data
            self.airport_code_label.config(text=f"Airport code: {data[0]}")
            self.flights_amount_label.config(text=f"Amount of flights: {data[1]}")
            self.mean_ammount_of_for_month_flights.config(text=f"Mean amount of flights per month: {data[2]}")
            self.mean_delay_label.config(text=f"Mean delay time: {data[3]}")
    
    def switch_button_set(self):
        if self.current_set == 1:
            self.button_set_1.pack_forget()
            self.button_set_2.pack(fill=tk.X, pady=7.5)
            self.current_set = 2
        else:
            self.button_set_2.pack_forget()
            self.button_set_1.pack(fill=tk.X, pady=7.5)
            self.current_set = 1

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

    def chartButton1(self):
        query = "SELECT * FROM flight_stats LIMIT 1000"
        results = self.execute_query(query)
        chosenAirportData = self.transform_data(results)

        xData, yData = generateChartDelayArrival(chosenAirportData)
        combinedData = list(zip(xData, yData))

        self.update_chart_callback(combinedData, 'Airport code', 'Delay Time (minutes)', 'Average Arival Delay Time (minutes)')

    def chartButton2(self):
        query = "SELECT * FROM flight_stats LIMIT 1000"
        results = self.execute_query(query)
        chosenAirportData = self.transform_data(results)

        xData, yData = generateChartDelayDeparture(chosenAirportData)
        combinedData = list(zip(xData, yData))

        self.update_chart_callback(combinedData, 'Airport code', 'Delay Time (minutes)', 'Average Departure Delay Time (minutes)')
    
    def chartButton4(self):
        query = "SELECT * FROM flight_stats LIMIT 1000"
        results = self.execute_query(query)

        xData, yData = plot_flights_per_month(results)
        combinedData = list(zip(xData, yData))
        self.update_chart_callback(combinedData, 'Date', 'Ammount of flights', 'Flights per month')

    def chartButton5(self):
        query = "SELECT * FROM flight_stats LIMIT 1000"
        results = self.execute_query(query)
        chosenAirportData = self.transform_data(results)

        xData, yData = generateChartAmountOfFlights123(results)
        combinedData = list(zip(xData, yData))

        self.update_chart_callback(combinedData, 'Airport code', 'Flights', 'Amount of Flights per Airport')

    def chartButton6(self):
        query = "SELECT * FROM flight_stats LIMIT 1000"
        results = self.execute_query(query)
        chosenAirportData = self.transform_data(results)

        xData, yData = generateChartAmountOfAD_Flights(results, 'Arrival')
        print(xData)
        print(yData)
        combinedData = list(zip(xData, yData))
        print(combinedData)

        self.update_chart_callback(combinedData, 'Airport code', 'Flights', 'Amount of Arrivals per Airport')

    def chartButton7(self):
        query = "SELECT * FROM flight_stats LIMIT 1000"
        results = self.execute_query(query)
        chosenAirportData = self.transform_data(results)

        xData, yData = generateChartAmountOfAD_Flights(results, 'Departure')
        print(xData)
        print(yData)
        combinedData = list(zip(xData, yData))
        print(combinedData)

        self.update_chart_callback(combinedData, 'Airport code', 'Flights', 'Amount of Departures per Airport')


    def new_file(self):
        query = "SELECT * FROM flight_stats LIMIT 100"
        results = self.execute_query(query)
        print(" ")
        print(" ")
        #print(results)
        print(" ")
        print(" ")
        with open('results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(results)

    def search_info(self):
        # Get the search term
        selected_index = self.search_results.curselection()

        # If an item is selected, get the item and use it as the search term
        if selected_index:
            search_term = self.search_results.get(selected_index)
            self.search_term.set(search_term)

        # Get the start date
        start_date = self.start_date.get()

        # Get the departure date
        departure_date = self.departure_date.get()

        # Get the data count
        data_count = self.data_count.get()

        # Call the callback function with the search information
        if self.search_info_callback:
            self.search_info_callback(search_term, start_date, departure_date, data_count)

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


    def transform_data(self, results):
        statList = []
        chosenAirportData = []

        for index, airport_code in enumerate(airport_codes):
            airportData = choose_data_by_airport(results, airport_code)
            # print(index, ". ", airportData)
            if (len(airportData) == 0):
                continue

            stat = calculate_statistics(airportData)

            statList.append([airport_code, stat])

        testData = get_some_elements_from_list(statList)
        chosenAirportData = choose_data_by_airport(results, airport_code)

        return testData
    
    def quit_app(self):
        self.quit()