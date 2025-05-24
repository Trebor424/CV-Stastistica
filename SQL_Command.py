
# -*- coding: utf-8 -*-
import pyodbc  # Import pyodbc for SQL Server connection
import Project_Classes  # Import custom classes
import os  # Import os module for path operations

# SQL query strings (placeholders - actual queries are not provided here)
SQL_Host_Product_Search_init = """

"""

SQL_Host_Product_Search = """

"""

SQL_Product_Search = """ 

    """
SQL_FPT_Testers_List = """

  """
SQL_ICT_Testers_List = """ 

  """

SQL_FFT_Testers_List = """

    """
SQL_FPT_ICT_FFT_Product_List = """

  """

SQL_serialnumber_masterid_search_FPT_board = """

"""

SQL_serialnumber_masterid_search_FPT_panels = """

"""

SQL_serialnumber_masterid_search_ICT_singleboard = """

"""
SQL_serialnumber_masterid_search_ICT_panels = """

"""

SQL_serialnumber_masterid_search_FFT = """

"""

### Main SQL FUNCTIONS
# Dictionary of designators for unit conversion (e.g., T for Tera, G for Giga)
Designators = {
    'T': 1000000000000,
    'G': 1000000000,
    'M': 1000000,
    'k': 1000,
    'm': 0.001,
    'u': 0.000001,
    'n': 0.000000001,
    'p': 0.000000000001,
}


###

def database_init(selected_server: str):
    # Connection string for SQL Server
    conn_str = (
        f'DRIVER={{SQL Server}};'
        f'SERVER={selected_server};'
        'Trusted_Connection=yes'  # Use Windows authentication
    )

    databases = []  # List to store retrieved database names

    try:
        # Connect to the SQL Server
        with pyodbc.connect(conn_str) as connection:
            # Create a cursor from the connection
            cursor = connection.cursor()

            # Execute the query to retrieve the list of databases
            query = "SELECT name FROM sys.databases"
            cursor.execute(query)

            # Fetch the results and store database names
            databases = [row[0] for row in cursor.fetchall()]

            # Filter and add databases with "-" in their name (this line has a potential bug: 'selected_server' is a string, not an object with 'filtered_databases' attribute)
            selected_server.filtered_databases = [db for db in databases if
                                                  "-" in db]  # This line will cause an AttributeError
            print(selected_server.filtered_databases)  # This will also fail due to the above AttributeError

    except Exception as e:
        print(f"Error connecting to the database: {e}")  # Print any connection errors

    return databases  # Return the list of databases


def tester_init(selected_server: str, selected_database: str, selected_process: str) -> list[str]:
    # Connection string for SQL Server with specified database
    conn_str = (
        f'DRIVER={{SQL Server}};'
        f'DATABASE={selected_database};'
        f'SERVER={selected_server};'
        'Trusted_Connection=yes'
    )

    Tester_database = []  # List to store tester information
    connection = None  # Initialize connection to None for finally block

    try:
        # Connect to the SQL Server
        connection = pyodbc.connect(conn_str)

        # Create a cursor from the connection
        cursor = connection.cursor()

        # Select the appropriate SQL query based on the selected process
        if selected_process == "ICT":
            query = SQL_ICT_Testers_List
            print("ICT")

        elif selected_process == "FPT":
            query = SQL_FPT_Testers_List
            print("FPT")

        elif selected_process == "FFT":
            query = SQL_FFT_Testers_List
            print("FFT")

        # Execute the query
        cursor.execute(query)

        # Fetch the results and populate Tester_database
        for row in cursor.fetchall():
            product_dict = {
                'id': row[0],
                'host': row[1],
            }
            Tester_database.append(product_dict)
            # print(f"Tester database - {product_dict}")


    except Exception as e:
        print(f"Error connecting to the database: {e}")  # Print any connection errors
    finally:
        # Close the connection in the 'finally' block to ensure it's always closed
        if connection:
            connection.close()
    return Tester_database  # Return the list of tester data


def Products_init_new(selected_server: str, selected_database: str, selected_process: str, selected_host: str,
                      start_time: str, end_time: str) -> list[str]:
    # Connection string for SQL Server
    conn_str = (
        f'DRIVER={{SQL Server}};'
        f'DATABASE={selected_database};'
        f'SERVER={selected_server};'
        'Trusted_Connection=yes'
    )

    Product_database = []  # List to store product information
    Product_database_verify_listy = []  # List for product verification
    connection = None  # Initialize connection to None

    try:
        query = SQL_Product_Search  # Use the SQL query for product search

        # Connect to the SQL Server
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()
        cursor.execute(query)  # Execute the product search query
        print(query)  # Print the query for debugging

        # Fetch results and populate Product_database
        for row in cursor.fetchall():
            Product_database_dict = {
                'skidprefix': row[0],
                'serialnumberprefix': row[1],
                'lasermarking': row[2],
                'productpartnumber': row[3],
                'panelnumberprefix': row[4],
                'numberofboards': row[5],
                'valid': row[6],
                'productpartnumber': row[7],  # This key is duplicated, might overwrite previous value
            }
            Product_database.append(Product_database_dict)

        # SQL query to get distinct scanned numbers within a timestamp range and host ID
        query2 = f'''
        select distinct scannednumber 
        from vREG_OF_PROCESS
        '''
        query2 += f" where timestamp between '{start_time}' AND '{end_time}' AND hostid like {selected_host}"

        cursor2 = connection.cursor()  # Create a second cursor
        cursor2.execute(query2)  # Execute the second query
        print(query2)  # Print the query for debugging

        # Fetch scanned numbers for verification
        for row in cursor2.fetchall():
            Product_database_verify_listy.append(row[0])
        # print(Product_database_verify_listy)

        # Print elements of Product_database (for debugging)
        for element in Product_database:
            print(f"{element['lasermarking']};{element['serialnumberprefix']};{element['panelnumberprefix']}")

        verified_products = []  # List to store verified products
        # Verify products based on panel or serial number prefixes
        for element in Product_database:
            for element_product_database in Product_database_verify_listy:
                if element['panelnumberprefix'] in element_product_database:
                    if element not in verified_products:
                        verified_products.append(element)
                elif element['serialnumberprefix'] in element_product_database:
                    if element not in verified_products:
                        verified_products.append(element)

                # print(f"{element['panelnumberprefix']}               {element['serialnumberprefix']}")

        # Open and read product names from a text file specific to the selected database
        with open(os.path.join(os.path.dirname(__file__), "Nazwy_wyrobow", f"{selected_database}.txt"), 'r') as file:
            zawartosc = file.readlines()  # Read all lines

        # Parse each line to update product 'lasermarking' if empty
        for line in zawartosc:
            try:
                name, serial_number, panel_number = line.strip().split(';')  # Split by semicolon
                # Check if the line contains at least three non-empty values
                if len(name) > 0 and len(serial_number) > 0 and len(panel_number) > 0:
                    for element in verified_products:
                        # Update 'lasermarking' if it's empty and a match is found by panel or serial number
                        if (len(element['lasermarking']) == 0 and (panel_number in element['panelnumberprefix']) or (
                                serial_number in element['serialnumberprefix'])):
                            element['lasermarking'] = name

                else:
                    print("Incomplete line:", line)  # Warn about incomplete lines
            except ValueError:
                print("Invalid line format:", line)  # Warn about invalid line format

    except Exception as e:
        print(f"Error connecting to the database: {e}")  # Print any connection errors
    finally:
        if connection:
            connection.close()  # Ensure connection is closed
    return verified_products  # Return the list of verified products


def test_databases(selected_server: str, selected_database: str, selected_process: str, selected_host: str,
                   start_time: str, end_time: str, serial_number_prefix: str, panel_number_prefix: str) -> list[str]:
    # Connection string for SQL Server
    conn_str = (
        f'DRIVER={{SQL Server}};'
        f'DATABASE={selected_database};'
        f'SERVER={selected_server};'
        'Trusted_Connection=yes'
    )

    Pan_Ser_numberdict = []  # List to store product test data
    connection = None  # Initialize connection to None

    # print(f"{selected_server} , {selected_database}, {selected_process}, {selected_host}, {start_time}, {end_time}")

    try:
        # Connect to the SQL Server
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()

        # Logic for ICT process
        if selected_process == "ICT":

            query = SQL_serialnumber_masterid_search_ICT_singleboard
            query += f" where REG_OF_TEST_ICT.timestamp between '{start_time}' AND '{end_time}'  AND serialnumber like '{serial_number_prefix}%' "
            query += f"AND maxvalue not like 'NULL' AND minvalue not like 'NULL' AND measuredvalue not like 'NULL'"  # Filter out NULL values
            print(query)  # Print query for debugging
            cursor.execute(query)  # Execute query

            Zmienna = cursor.fetchall()  # Fetch all results

            if not len(Zmienna) == 0:  # If results for single board exist

                for row in Zmienna:
                    # Create a Wyrob object and append to list
                    Wyrob = Project_Classes.Wyrob(
                        row[0],  # masterid
                        row[1],  # panel/serialnumber
                        row[2],  # boardsnumber
                        row[3],  # parts
                        "",  # aux (empty for ICT)
                        "",  # value (empty for ICT)
                        "",  # loc (empty for ICT)
                        "",  # el (empty for ICT)
                        row[5],  # reference
                        row[6],  # +%
                        row[7],  # -%
                        row[9],  # timestamp
                        row[8],  # measured value
                        "ICT"
                    )

                    # print(f"{Wyrob.parts} + {Wyrob.value}")
                    # print(f"-{Wyrob.tolerance_minus} = {Wyrob.value} = +{Wyrob.tolerance_plus}")
                    Pan_Ser_numberdict.append(Wyrob)

            else:  # If no results for single board, try panels

                query = SQL_serialnumber_masterid_search_ICT_panels
                query += f" where REG_OF_TEST_ICT.timestamp between '{start_time}' AND '{end_time}'  AND panelorserialnumber like '{panel_number_prefix}%' "
                query += f"AND maxvalue not like 'NULL' AND minvalue not like 'NULL' AND measuredvalue not like 'NULL'"  # Filter out NULL values
                print(query)  # Print query for debugging
                cursor.execute(query)  # Execute query

                for row in cursor.fetchall():
                    # Create a Wyrob object and append to list
                    Wyrob = Project_Classes.Wyrob(
                        row[0],  # masterid
                        row[1],  # panelorseialnumber
                        row[2],  # boardsnumber
                        row[3],  # parts
                        "",  # aux (empty for ICT)
                        "",  # value (empty for ICT)
                        "",  # loc (empty for ICT)
                        "",  # el (empty for ICT)
                        row[5],  # reference
                        row[6],  # +%
                        row[7],  # -%
                        row[9],  # timestamp
                        row[8],  # measured value
                        "ICT"
                    )

                    # print(f"{Wyrob.parts} + {Wyrob.value}")
                    # print(f"-{Wyrob.tolerance_minus} = {Wyrob.value} = +{Wyrob.tolerance_plus}")
                    Pan_Ser_numberdict.append(Wyrob)


        # Logic for FPT process
        elif selected_process == "FPT":
            query = SQL_serialnumber_masterid_search_FPT_board
            query += f" where timestamp between '{start_time}' AND '{end_time}'  AND serialnumber like '{serial_number_prefix}%'  AND judge not like 'SKIP'"  # Filter out 'SKIP' judgments

            cursor.execute(query)  # Execute query
            Zmienna = cursor.fetchall()  # Fetch all results
            # print(cursor.fetchall())

            if not len(Zmienna) == 0:  # If results for FPT board exist

                query = SQL_serialnumber_masterid_search_FPT_board
                query += f""" where timestamp between '{start_time}' AND '{end_time}'  AND serialnumber like '{serial_number_prefix}%'  
                AND judge NOT LIKE 'SKIP' 
                AND loc in ('KELV','RES','CAP','IND') # Filter by specific locations
                AND [-%] not like '0' 
                AND [+%] not like '0'
                AND judge = 'PASS' # Only include 'PASS' judgments
                """
                cursor.execute(query)  # Execute refined query
                print(query)  # Print query for debugging

                for row in cursor.fetchall():
                    # print(row)
                    # i=0
                    # for element in row:
                    #     print(f"{i}  ==== {row[i]}")
                    #     i+=1

                    Valuereference = row[10]  # Get reference value
                    # Apply designator multiplier to reference value
                    for element in Designators:
                        if element in row[11]:  # Check if designator is in the unit string
                            Valuereference *= Designators[element]

                    Valuevariable = 0
                    # Determine measured value and apply designator multiplier
                    if row[18] == '':
                        Valuevariable = row[15]  # testValue
                        # print(f"INIT Valuevariable ---------> {Valuevariable}")
                        for element in Designators:
                            if element in row[16]:  # Check if designator is in the unit string
                                Valuevariable *= Designators[element]
                    else:
                        Valuevariable = row[17]  # testValue
                        for element in Designators:
                            if element in row[18]:  # Check if designator is in the unit string
                                Valuevariable *= Designators[element]
                                # print(f"------------> Valuevariable {Valuevariable}  Element {element} Row {row[15]}")

                    # Calculate tolerance limits based on reference and percentage tolerance
                    tolerance_plus = Valuereference + (row[13] / 50) * Valuereference
                    tolerance_minus = Valuereference - (row[14] / 50) * Valuereference

                    # Create a Wyrob object and append to list
                    Wyrob = Project_Classes.Wyrob(
                        row[0],  # masterid
                        row[21],  # panel/serialnumber
                        row[1],  # boardsnumber
                        row[3],  # parts
                        row[4],  # aux
                        row[5],  # value
                        row[8],  # loc
                        row[9],  # el
                        row[10],  # reference (original string)
                        tolerance_plus,  # calculated +%
                        tolerance_minus,  # calculated -%
                        row[24],  # timestamp
                        Valuevariable,  # calculated measured value
                        "FPT_BOARD"
                    )

                    # print(f"{Wyrob.parts} + {Valuevariable}")
                    # print(f"-{Wyrob.tolerance_minus} = {Valuereference} = +{Wyrob.tolerance_plus}")
                    Pan_Ser_numberdict.append(Wyrob)

            else:  # If no results for FPT board, try FPT panels
                query = SQL_serialnumber_masterid_search_FPT_panels
                query += f""" WHERE timestamp BETWEEN '{start_time}' AND '{end_time}' AND panelnumber LIKE '{panel_number_prefix}%' 
                AND judge NOT LIKE 'SKIP' 
                AND loc in ('KELV','RES','CAP','IND') # Filter by specific locations
                AND [-%] not like '0' 
                AND [+%] not like '0'
                AND judge = 'PASS' # Only include 'PASS' judgments
                """
                cursor.execute(query)  # Execute query
                # print(panel_number_prefix)
                print(query)  # Print query for debugging

                for row in cursor.fetchall():

                    Valuereference = row[8]  # Get reference value
                    # Apply designator multiplier to reference value
                    for element in Designators:
                        if element in row[9]:
                            Valuereference *= Designators[element]

                    Valuevariable = 0
                    # Determine measured value and apply designator multiplier
                    if row[16] == '':
                        Valuevariable = row[13]
                        for element in Designators:
                            if element in row[14]:
                                Valuevariable *= Designators[element]
                    else:
                        Valuevariable = row[15]  # testValue
                        for element in Designators:
                            if element in row[16]:
                                Valuevariable *= Designators[element]

                    # Calculate tolerance limits based on reference and percentage tolerance
                    tolerance_plus = Valuereference + (row[11] / 50) * Valuereference
                    tolerance_minus = Valuereference - (row[12] / 50) * Valuereference

                    # Create a Wyrob object and append to list
                    Wyrob = Project_Classes.Wyrob(
                        row[0],  # masterid
                        row[18],  # panel/serialnumber
                        row[1],  # boardsnumber
                        row[3],  # parts
                        row[4],  # aux
                        row[5],  # value
                        row[6],  # loc
                        row[7],  # el
                        row[8],  # reference (original string)
                        tolerance_plus,  # calculated +%
                        tolerance_minus,  # calculated -%
                        row[22],  # timestamp
                        Valuevariable,  # calculated measured value
                        "FPT_PANEL"
                    )

                    # print(f"{Wyrob.parts} + {Valuevariable}")
                    # print(f"-{Wyrob.tolerance_minus} = {Valuereference} = +{Wyrob.tolerance_plus}")
                    Pan_Ser_numberdict.append(Wyrob)


        # Logic for FFT process
        elif selected_process == "FFT":
            query = SQL_serialnumber_masterid_search_FFT
            query += f" where timestamp between '{start_time}' AND '{end_time}'  AND serialnumber like '{serial_number_prefix}%' AND teststep not like '%ontaz%' "
            # 'monta�' (assembly) is excluded from test steps

            print(query)  # Print query for debugging
            cursor.execute(query)  # Execute query

            for row in cursor.fetchall():
                # print(row)

                i = 0
                for element in row:
                    # print(f"{i}  ==== {row[i]}")
                    i += 1

                # Create a Wyrob object and append to list
                Wyrob = Project_Classes.Wyrob(
                    row[0],  # masterid
                    row[1],  # panel/serialnumber
                    1,  # boardsnumber (set to 1 for FFT)
                    row[2],  # parts
                    1,  # aux (set to 1 for FFT)
                    1,  # value (set to 1 for FFT)
                    1,  # loc (set to 1 for FFT)
                    1,  # el (set to 1 for FFT)
                    1,  # reference (set to 1 for FFT)
                    row[4],  # +%
                    row[3],  # -%
                    row[6],  # timestamp
                    row[5],  # measured value
                    "FFT"
                )

                # print(f"{Wyrob.parts} + {Wyrob.value}")
                # print(f"-{Wyrob.tolerance_minus} = {Wyrob.value} = +{Wyrob.tolerance_plus}")
                Pan_Ser_numberdict.append(Wyrob)
    except Exception as e:
        print(f"Error connecting to the database or processing data: {e}")  # Catch any exceptions
    finally:
        if connection:
            connection.close()  # Ensure connection is closed
    return Pan_Ser_numberdict  # Return the list of product test data