import SQL_Command
import Math_source

import json
import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

# Dictionary to store chart results (currently unused but declared)
dict_chart_result = {}


class MainForm:

    def __init__(self, root):

        self.root = root
        # Configure the main window settings
        self.configure_window()
        # Initialize form comboboxes (server and database selection)
        self.init_forms_combobox()
        # Initialize process combobox (testing process selection)
        self.init_proces_combobox()
        # Initialize date selection widgets
        self.init_time_select()
        # Initialize the Treeview for manufacturing data
        self.init_treeviews_manufacture()
        # Initialize the Treeview for test results
        self.init_treeviews_tests()
        # Initialize host computer selection combobox
        self.init_host_comp_select()
        # Initialize the search button
        self.init_search_button()
        # Create the toggle switch for displaying groups
        self.create_toggle_switch()

    def configure_window(self):
        # Set the window size
        self.root.geometry("1500x800")
        # Set the window title
        self.root.title("Statistica")

    def create_toggle_switch(self):
        # File to save toggle switch status
        self.STATE_FILE = 'toggle_switch_state.json'

        # Function to save the state of the switch
        def save_state(state):
            with open(self.STATE_FILE, 'w') as f:
                json.dump(state, f)

        # Function to read the state of the switch from file
        def load_state():
            if os.path.exists(self.STATE_FILE):
                with open(self.STATE_FILE, 'r') as f:
                    return json.load(f)
            # Return default state if file does not exist
            return {'toggle_state': False}

        # Function to toggle the switch status
        def toggle_switch():
            self.toggle_state = not self.toggle_state
            # Save the new state
            save_state({'toggle_state': self.toggle_state})
            # Update the button text based on the new state
            update_switch_text()

        # Function to update the switch text based on its status
        def update_switch_text():
            if self.toggle_state:
                toggle_button.config(text="Wylaczone")  # "Disabled"
            else:
                toggle_button.config(text="Wlaczone")  # "Enabled"

        # Load the initial state from the file
        state = load_state()
        self.toggle_state = state['toggle_state']

        # Create switch style
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 16))

        # Create label for the toggle switch
        toggle_button_label = tk.Label(self.root, text="Wyswietlanie Grup", font=("Arial", 12))
        toggle_button_label.grid(row=9, column=0, padx=10, pady=10)

        # Create the toggle button
        toggle_button = ttk.Button(self.root, text="", command=toggle_switch, style='TButton')
        toggle_button.grid(row=10, column=0, padx=10, pady=10)  # Place the switch on the grid in the main window

        # Load the first status to set initial button text
        update_switch_text()

    def init_search_button(self):
        # Create and place the search button
        search_button = tk.Button(self.root, text="Wyszukaj", command=self.on_search_button_click)
        search_button.grid(row=1, column=7, padx=10, pady=10)

    def init_forms_combobox(self):
        # Label for server selection
        server_label = tk.Label(self.root, text="Wybierz Serwer ", font=("Arial", 12))
        server_label.grid(row=1, column=0, padx=10, pady=10)

        # Values for server combobox
        server_combobox_values = ["serwerName"]
        # Create and place the server combobox
        self.server_combobox = ttk.Combobox(self.root, values=server_combobox_values)
        # Set default value for server combobox
        self.server_combobox.set("serwerName")
        self.server_combobox.grid(row=2, column=0, padx=10, pady=10)

        # Label for database selection
        database_label = tk.Label(self.root, text="Wybierz Baze Danych: ", font=("Arial", 12))
        database_label.grid(row=3, column=0, padx=10, pady=10)

        # Values for database combobox (commented out fetching from SQL_Command)
        database_combobox_values = ["Nazwa1", "Nazwa2", "Nazwa3"]
        # database_combobox_values =SQL_Command.database_init(self.get_selected_server)
        # Create and place the database combobox
        self.database_combobox = ttk.Combobox(self.root, values=database_combobox_values)
        # self.database_combobox.set("PCCI-kopia")
        self.database_combobox.grid(row=4, column=0, padx=10, pady=10)

    def init_proces_combobox(self):
        # Label for process selection
        process_label = tk.Label(self.root, text="Wybierz Proces Testowania", font=("Arial", 12))
        process_label.grid(row=1, column=2, padx=10, pady=10)

        # Values for process combobox
        process_combobox_values = ["FPT", "ICT", "FFT"]
        # Create and place the process combobox
        self.process_combobox = ttk.Combobox(self.root, values=process_combobox_values)
        self.process_combobox.grid(row=1, column=3, padx=10, pady=10)

        # Add action to combobox when selected
        self.process_combobox.bind("<<ComboboxSelected>>", self.on_combobox_selected)

    def init_host_comp_select(self):
        # Label for machine selection
        machine_label = tk.Label(self.root, text="Wybierz Hosta", font=("Arial", 12))
        machine_label.grid(row=1, column=4, padx=10, pady=10)

        # Create and place the machine combobox
        self.machine_combobox = ttk.Combobox(self.root)
        self.machine_combobox.grid(row=1, column=5, padx=10, pady=10)

        # Add action after binding of combobox element
        self.machine_combobox.bind("<<ComboboxSelected>>", self.on_combobox_selected)

    def init_time_select(self):
        # Label for start date selection
        start_date_label = tk.Label(self.root, text="Wybierz date od kiedy: ", font=("Arial", 12))
        start_date_label.grid(row=5, column=0, padx=10, pady=10)

        # Create and place the start date entry widget
        self.start_date_entry = DateEntry(self.root, width=14, background="darkblue", foreground="white", borderwidth=4,
                                          date_pattern="dd/mm/yy")
        self.start_date_entry.grid(row=6, column=0, padx=10, pady=10)
        # Set initial start date (60 days ago)
        self.start_date_entry.set_date(datetime.now() - timedelta(days=60))

        # Label for end date selection
        end_date_label = tk.Label(self.root, text="Wybierz date do kiedy: ", font=("Arial", 12))
        end_date_label.grid(row=7, column=0, padx=10, pady=10)

        # Create and place the end date entry widget
        self.end_date_entry = DateEntry(self.root, width=14, background="darkblue", foreground="white", borderwidth=4,
                                        date_pattern="dd/mm/yy")
        self.end_date_entry.grid(row=8, column=0, padx=10, pady=10)

    def init_treeviews_manufacture(self):
        # Replace the Listbox with a Treeview for manufacturing data
        self.treeview1 = ttk.Treeview(self.root, height=35, columns=("Name", "PanelPrefix", "SerialNumberPrefix"),
                                      show="headings")

        # Define column headings and sorting commands for Treeview1
        self.treeview1.heading("Name", text="Name", command=lambda: self.sort_treeview_string(self.treeview1, "Name"))
        self.treeview1.heading("PanelPrefix", text="PanelPrefix",
                               command=lambda: self.sort_treeview_string(self.treeview1, "PanelPrefix"))
        self.treeview1.heading("SerialNumberPrefix", text="SerialNumberPrefix",
                               command=lambda: self.sort_treeview_string(self.treeview1, "SerialNumberPrefix"))

        # Set column widths for Treeview1
        self.treeview1.column("Name", width=100)
        self.treeview1.column("PanelPrefix", width=100)
        self.treeview1.column("SerialNumberPrefix", width=200)
        # Place Treeview1 on the window
        self.treeview1.place(x=200, y=40)
        # Bind double-click event to Treeview1
        self.treeview1.bind("<Double-Button-1>", self.on_treeviews_manufacture_click)

        # Create and place scrollbar for Treeview1
        scrollbar_treeview1 = ttk.Scrollbar(self.root, orient="vertical", command=self.treeview1.yview)
        scrollbar_treeview1.place(x=605, y=40, height=725)
        # Configure Treeview1 to use the scrollbar
        self.treeview1.configure(yscrollcommand=scrollbar_treeview1.set)

    def init_treeviews_tests(self):
        # Initialize Treeview for test results
        self.treeview2 = ttk.Treeview(self.root, height=35, columns=(
        "Fixture", "Test_Name", "Group", "CP", "CPK", "PP", "PPK", "O_stand", "Limit_Change"), show="headings")
        # Define column headings and sorting commands for Treeview2
        self.treeview2.heading("Fixture", text="Fixture",
                               command=lambda: self.sort_treeview_string(self.treeview2, "Fixture"))
        self.treeview2.heading("Test_Name", text="Test_Name",
                               command=lambda: self.sort_treeview_string(self.treeview2, "Test_Name"))
        self.treeview2.heading("Group", text="Group", command=lambda: self.sort_treeview_value(self.treeview2, "Group"))
        self.treeview2.heading("CP", text="CP", command=lambda: self.sort_treeview_value(self.treeview2, "CP"))
        self.treeview2.heading("CPK", text="CPK", command=lambda: self.sort_treeview_value(self.treeview2, "CPK"))
        self.treeview2.heading("PP", text="PP", command=lambda: self.sort_treeview_value(self.treeview2, "PP"))
        self.treeview2.heading("PPK", text="PPK", command=lambda: self.sort_treeview_value(self.treeview2, "PPK"))
        self.treeview2.heading("O_stand", text="O_stand",
                               command=lambda: self.sort_treeview_value(self.treeview2, "O_stand"))
        self.treeview2.heading("Limit_Change", text="Limit_Change",
                               command=lambda: self.sort_treeview_string(self.treeview2, "Limit_Change"))

        # Set column widths for Treeview2
        self.treeview2.column("Fixture", width=50)
        self.treeview2.column("Test_Name", width=150)
        self.treeview2.column("Group", width=50)
        self.treeview2.column("CP", width=50)
        self.treeview2.column("CPK", width=50)
        self.treeview2.column("PP", width=50)
        self.treeview2.column("PPK", width=50)
        self.treeview2.column("O_stand", width=100)
        self.treeview2.column("Limit_Change", width=100)

        # Bind selection event to Treeview2 to create charts
        self.treeview2.bind("<<TreeviewSelect>>", self.chart_charts_create)
        # Place Treeview2 on the window
        self.treeview2.place(x=640, y=40)

        # Create and place scrollbar for Treeview2
        scrollbar_treeview2 = ttk.Scrollbar(self.root, orient="vertical", command=self.treeview2.yview)
        scrollbar_treeview2.place(x=1295, y=40, height=725)
        # Configure Treeview2 to use the scrollbar
        self.treeview2.configure(yscrollcommand=scrollbar_treeview2.set)

    def chart_charts_create(self, event):
        # Close any open matplotlib plots
        plt.close()

        # Get selected item from Treeview2
        selected_items = self.treeview2.selection()

        if selected_items:
            # Get the ID of the selected row
            item_id = selected_items[0]
            # Get the index of the selected row
            item_index = self.treeview2.index(item_id)
            # Get the values of the selected row
            item_values = self.treeview2.item(item_id)
            # Extract test name
            test_name = item_values['values'][1]

            # Get selected item from Treeview1
            selected_items2 = self.treeview1.selection()
            item_id2 = selected_items2[0]
            item_values2 = self.treeview1.item(item_id2)
            # Extract board name
            board_name = item_values2['values'][0]

            # Check the state of the toggle switch
            if self.toggle_state is True:
                # If toggle is ON (Wylaczone - "Disabled", meaning displaying groups individually)
                with open('calculate_magazine.txt', 'r') as file:
                    for num, line in enumerate(file, 1):
                        if test_name in line:
                            Dane = line.split(';')
                            print(Dane, self)
                            Math_source.Chart_create(Dane)
                    Dane = []

            elif self.toggle_state is False:
                # If toggle is OFF (Wlaczone - "Enabled", meaning grouping is enabled)
                print("Nie skonczyles")  # This message seems to indicate unfinished functionality
                test_name = test_name[:-2]  # Adjust test name for grouping
                with open('calculate_magazine.txt', 'r') as file:
                    dict_values = {}
                    i = 0
                    for num, line in enumerate(file, 1):
                        if test_name in line:
                            i = i + 1
                            Dane = line.split(';')
                            print(Dane, self)
                            # list_values.append(Dane)
                            dict_values[f"List_{i}"] = Dane
                    Math_source.Chart_create_group(dict_values)

        # This block seems to be a duplicate of the one above.
        selected_items = self.treeview2.selection()
        if selected_items:
            # Get the ID of the selected row
            item_id = selected_items[0]
            item_index = self.treeview2.index(item_id)
            item_values = self.treeview2.item(item_id)
            test_name = item_values['values'][1]

            selected_items2 = self.treeview1.selection()
            item_id2 = selected_items2[0]
            item_values2 = self.treeview1.item(item_id2)
            board_name = item_values2['values'][0]

    def add_to_treeview1_manufacture(self, values):
        # Insert values into the manufacturing Treeview
        self.treeview1.insert("", tk.END, values=values)

    def add_to_treeview2_testresult(self, values):
        # Insert values into the test results Treeview (seems to be a duplicate of add_to_treeview_test)
        self.treeview2.insert("", tk.END, values=values)

    def clear_to_treeview_manufacture(self):
        # Delete all items from the manufacturing Treeview
        self.treeview1.delete(*self.treeview1.get_children())

    def clear_to_treeview_tests(self):
        # Delete all items from the test results Treeview
        self.treeview2.delete(*self.treeview2.get_children())

    def add_to_treeview_test(self, values):
        # Insert values into the test results Treeview
        self.treeview2.insert("", tk.END, values=values)

    def on_treeviews_manufacture_click(self, event):

        # Clear the second treeview (test results)
        self.clear_to_treeview_tests()

        # Get selected item from Treeview1
        selected_items = self.treeview1.selection()

        if selected_items:
            item_id = selected_items[0]

            Test_Proces_Values = self.treeview1.item(item_id, "values")
        # Extract serial and panel prefixes and name
        serial_number_prefix = Test_Proces_Values[2]
        panel_number_prefix = Test_Proces_Values[1]
        Name = Test_Proces_Values[0]

        # Fetch test databases using SQL_Command
        test_databases = SQL_Command.test_databases(self.get_selected_server(), self.get_selected_database(),
                                                    self.get_selected_process(), self.get_selected_host(),
                                                    self.get_selected_start_date(), self.get_selected_end_date(),
                                                    serial_number_prefix, panel_number_prefix)

        # Compare tests using Math_source
        compare_tests = Math_source.Compare_tests(test_databases)

        # Delete test_databases to free memory
        del test_databases

        # Calculate CP, CPK, PP, PPK, O_stand using Math_source
        test_results = Math_source.calculate_cp_cpk_pp_ppk_o_stand(compare_tests, self.get_selected_database(), Name)
        # Delete compare_tests to free memory
        del compare_tests

        # Add calculated test results to the test results Treeview
        for element in test_results:
            try:
                self.add_to_treeview_test(
                    [element.fixture,
                     element.testname,
                     element.group,
                     element.cp,
                     element.cpk,
                     element.pp,
                     element.ppk,
                     element.o_stand,
                     element.limitchange])
            except:
                NameError()  # This error handling is very generic and not ideal

    def sort_treeview_string(self, tree, col, reverse=False):
        # Sort Treeview by string column
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=reverse)
        for index, (val, child) in enumerate(data):
            tree.move(child, '', index)
        # Toggle sort order for next click
        tree.heading(col, command=lambda: self.sort_treeview_string(tree, col, not reverse))

    def sort_treeview_value(self, tree, col, reverse=False):
        # Sort Treeview by numeric (float) column
        data = [(float(tree.set(child, col)), child) for child in tree.get_children('')]
        data.sort(reverse=reverse)
        for index, (val, child) in enumerate(data):
            tree.move(child, '', index)
        # Toggle sort order for next click
        tree.heading(col, command=lambda: self.sort_treeview_value(tree, col, not reverse))

    def get_selected_server(self):
        # Get the selected server from the combobox
        return self.server_combobox.get()

    def get_selected_host(self):
        # Get the selected host from the combobox
        return self.machine_combobox.get()

    def get_selected_database(self):
        # Get the selected database from the combobox
        return self.database_combobox.get()

    def get_selected_process(self):
        # Get the selected process from the combobox
        return self.process_combobox.get()

    def get_selected_start_date(self):
        # Get the selected start date from the entry widget
        start_date_str = self.start_date_entry.get()

        try:
            # Parse the date string to a datetime object
            start_date = datetime.strptime(start_date_str, "%d/%m/%y")
            return start_date
        except ValueError:
            print("Blad: Nieprawidlowy format daty")  # "Error: Invalid date format"
            return None

    def get_selected_end_date(self):
        # Get the selected end date from the entry widget
        end_date_str = self.end_date_entry.get()

        try:
            # Parse the date string to a datetime object
            end_date = datetime.strptime(end_date_str, "%d/%m/%y")
            return end_date
        except ValueError:
            print("Blad: Nieprawidlowy format daty")  # "Error: Invalid date format"
            return None

    # Function which takes value of combobox
    def on_combobox_selected(self, event):

        # Print selected values (for debugging/info)
        selected_server = self.get_selected_server()
        print("Wybrany Serwer:", selected_server),  # "Selected Server:"

        selected_database = self.get_selected_database()
        print("Wybrana Baza Danych:", selected_database)  # "Selected Database:"

        selected_process = self.get_selected_process()
        print("Wybrany Proces Testowania:", selected_process)  # "Selected Testing Process:"

        start_date = self.get_selected_start_date()
        print("Data poczatkowa:", start_date)  # "Start Date:"

        end_date = self.get_selected_end_date()
        print("Data koncowa:", end_date)  # "End Date:"

        # Clear the manufacturing Treeview
        self.clear_to_treeview_manufacture()

        # Initialize tester data from SQL_Command
        Tester_database = SQL_Command.tester_init(self.get_selected_server(), self.get_selected_database(),
                                                  self.get_selected_process())

        # Populate machine combobox with host values from tester data
        values_to_add = []
        for element in Tester_database:
            values_to_add.append(list(element.values())[1])
        self.machine_combobox['values'] = values_to_add

    def on_search_button_click(self):

        # Clear the manufacturing Treeview
        self.clear_to_treeview_manufacture()

        # Initialize tester data from SQL_Command
        Tester_database = SQL_Command.tester_init(self.get_selected_server(), self.get_selected_database(),
                                                  self.get_selected_process())

        # Find the selected host ID
        for element in Tester_database:
            if element['host'] == self.get_selected_host():
                print(f"{element['host']}                                           {self.get_selected_host()}")
                selected_host_id = element['id']

        # Initialize product data using SQL_Command
        product_database2 = SQL_Command.Products_init_new(self.get_selected_server(), self.get_selected_database(),
                                                          self.get_selected_process(), selected_host_id,
                                                          self.get_selected_start_date(), self.get_selected_end_date())
        # Add product data to the manufacturing Treeview
        for product in product_database2:
            Serialnumber = list(product.values())[1]
            self.add_to_treeview1_manufacture(
                [list(product.values())[2], list(product.values())[4], Serialnumber])  # [:-2]]

    def calculate_button_click(self):

        print("Wejscie w calculate button click")  # "Entering calculate button click"
        # Clear the test results Treeview
        self.clear_to_treeview_tests()

        # Get selected item from Treeview1 (currently unused after getting item_id)
        selected_items = self.treeview1.selection()
        if selected_items:
            item_id = selected_items[0]
            Test_Proces_Values = self.treeview1.item(item_id, "values")