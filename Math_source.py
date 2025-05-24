# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors
from scipy.stats import norm
from datetime import datetime

import Project_Classes


def Compare_tests(Pan_Ser_numberdict):
    test_dict = {}
    # Iterate through each item in the input dictionary
    for single_wyrob in Pan_Ser_numberdict:
        # Create a unique test name for each item
        test_name = f"{single_wyrob.parts}_{single_wyrob.aux}_{single_wyrob.value}_{single_wyrob.boardsnumber}"

        # If the test name is not in the dictionary, create a new entry
        if test_name not in test_dict:
            test_dict[test_name] = Project_Classes.Testy_wyrobow(
                single_wyrob.parts,
                single_wyrob.aux,
                single_wyrob.value,
                single_wyrob.boardsnumber,
                single_wyrob.loc,
                single_wyrob.el,
                [single_wyrob.reference],
                [single_wyrob.tolerance_plus],
                [single_wyrob.tolerance_minus],
                [single_wyrob.testvalue],
                [single_wyrob.timestamp]
            )
        # If the test name exists, append new data to the existing entry
        else:
            test_dict[test_name].reference.append(single_wyrob.reference)
            test_dict[test_name].tolerance_plus.append(single_wyrob.tolerance_plus)
            test_dict[test_name].tolerance_minus.append(single_wyrob.tolerance_minus)
            test_dict[test_name].listtestvalue[0].append(single_wyrob.testvalue)
            test_dict[test_name].listtestvalue[1].append(single_wyrob.timestamp)

    return test_dict


def calculate_cp_cpk_pp_ppk_o_stand(test_dict, test_database, name):
    test_result_list = []

    # Open 'calculate_magazine.txt' in write mode (clears content on open)
    with open('calculate_magazine.txt', 'w') as mag:
        # Truncate the file (redundant with 'w' mode but explicitly here)
        mag.truncate(0)
        # Iterate through each test in the test dictionary
        for test_name in test_dict:
            test = test_dict[test_name]
            # Convert tolerance and reference lists to sets to get unique values
            tolerance_plus_set = set(test.tolerance_plus)
            tolerance_minus_set = set(test.tolerance_minus)
            reference_set = set(test.reference)
            # Determine lower and upper specification limits
            lower_spec_limit = min(tolerance_minus_set)
            upper_spec_limit = max(tolerance_plus_set)
            # Check if limits have changed (i.e., multiple unique values exist)
            limitchange = "NO" if len(tolerance_minus_set) == 1 and len(tolerance_plus_set) == 1 and len(
                reference_set) == 1 else "YES"
            # Calculate mean and standard deviation of test values
            mean = np.mean(test.listtestvalue[0])
            std_dev = np.std(test.listtestvalue[0])

            # Calculate CP, CPK, PP, PPK, and O_stand (standard deviation)
            cp = round((upper_spec_limit - lower_spec_limit) / (6 * std_dev), 3)
            cpk = round(min((upper_spec_limit - mean) / (3 * std_dev), (mean - lower_spec_limit) / (3 * std_dev)), 3)
            pp = round(norm.cdf(upper_spec_limit, mean, std_dev) - norm.cdf(lower_spec_limit, mean, std_dev), 3)
            ppk = round(min((upper_spec_limit - mean) / (3 * std_dev), (mean - lower_spec_limit) / (3 * std_dev)), 3)
            o_stand = round(std_dev, 3)

            # Create a Wyniki_testow object with calculated results
            test_values = Project_Classes.Wyniki_testow(
                fixture=" ",
                testname=f"{test.parts}_{test.aux}_{test.value}_{test.boardsnumber}",  # boardsnumber added
                group=test.boardsnumber,
                cp=cp,
                cpk=cpk,
                pp=pp,
                ppk=ppk,
                o_stand=o_stand,
                limitchange=limitchange
            )
            # Add the test results to the list
            test_result_list.append(test_values)

            # Write results to the 'calculate_magazine.txt' file
            mag.writelines("      ")
            mag.write(
                f"{test.parts};{test.aux};{test.value};{test.boardsnumber};{test.loc};{test.el};{test.reference};{test.tolerance_plus};{test.tolerance_minus};{test.listtestvalue[0]};{test.listtestvalue[1]};")
            mag.write(
                f"{test_values.fixture};{test_values.testname};{test_values.group};{test_values.cp};{test_values.cpk};{test_values.pp};{test_values.ppk};{test_values.o_stand};{test_values.limitchange};{mean};\n")

            # print(f"{test.parts}_{test.aux}_{test.value}  cp: {cp}      cpk: {cpk}       pp: {pp}        ppk: {ppk}       o_stand: {o_stand}")

        return test_result_list


def Chart_create(Dane):
    # Turn on interactive mode for matplotlib
    plt.ion()

    # Parse input data
    parts = Dane[0]
    aux = Dane[1]
    value = Dane[2]
    # boardsnumber is expected to be a list of floats
    boardsnumber = [float(x) for x in Dane[3]]
    loc = Dane[4]
    el = Dane[5]
    # Parse list-like strings to actual lists of floats
    reference = [float(x) for x in Dane[6].replace('[', '').replace(']', '').split(',')]
    tolerance_plus = [float(x) for x in Dane[7].replace('[', '').replace(']', '').split(',')]
    tolerance_minus = [float(x) for x in Dane[8].replace('[', '').replace(']', '').split(',')]

    # Process timestamp string to a list of datetime objects
    Timestamp_list = Dane[10].replace('[', '').replace(']', '').split("),")
    New_Timestamp_list = []

    for element in Timestamp_list:
        New_Timestamp_list.append(f"{element})")

    New_Timestamp_list_2 = []

    for date in New_Timestamp_list:
        try:
            try:
                # Try parsing with microseconds
                date_str = datetime.strptime(
                    date.replace(" ", "").replace("datetime.datetime", "").replace("(", "").replace(")", ""),
                    "%Y,%m,%d,%H,%M,%S,%f")
            except:
                try:
                    # Try parsing without microseconds
                    date_str = datetime.strptime(
                        date.replace(" ", "").replace("datetime.datetime", "").replace("(", "").replace(")", ""),
                        "%Y,%m,%d,%H,%M,%S")
                except:
                    # Try parsing with only minutes
                    date_str = datetime.strptime(
                        date.replace(" ", "").replace("datetime.datetime", "").replace("(", "").replace(")", ""),
                        "%Y,%m,%d,%H,%M")
            New_Timestamp_list_2.append(date_str)
        except ValueError:
            print(f"Nieprawidlowy format daty -> {date}")  # "Invalid date format -> {date}"
        except Exception as e:
            print(f"Wystapil inny blad: {e}")  # "Another error occurred: {e}"

    # Combine test values and processed timestamps
    listtestvalue = [float(x) for x in Dane[9].replace('[', '').replace(']', '').split(',')], New_Timestamp_list_2

    # Extract remaining data, cleaning up string formatting
    testname = Dane[12]
    group = Dane[13]
    cp = float(Dane[14].replace('(', '').replace(')', '').replace(',', ''))
    cpk = float(Dane[15].replace('(', '').replace(')', '').replace(',', ''))
    pp = float(Dane[16].replace('(', '').replace(')', '').replace(',', ''))
    ppk = float(Dane[17].replace('(', '').replace(')', '').replace(',', ''))
    o_stand = float(Dane[18].replace('(', '').replace(')', '').replace(',', ''))
    limitchange = Dane[19].replace('(', '').replace(')', '').replace(',', '')
    mean = float(Dane[20].replace('(', '').replace(')', '').replace(',', ''))

    # Get unique tolerance limits
    tolerance_plus_set = set(tolerance_plus)
    tolerance_minus_set = set(tolerance_minus)
    upper_spec_limit = list(tolerance_plus_set)
    lower_spec_limit = list(tolerance_minus_set)

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Set the main title for the figure
    fig.suptitle(f"{parts}_{aux}_{value}_{group}")

    # Configure the left plot (histogram and normal distribution)
    ax1.set_xlabel('Wartosc')  # "Value"
    ax1.set_ylabel('Prawdopodobienstwo')  # "Probability"
    ax1.set_title('Rozklad danych i rozklad normalny')  # "Data distribution and normal distribution"
    ax1.grid(True)

    # Plot histogram of data
    ax1.hist(listtestvalue[0], bins=20, density=True, alpha=0.5, color='g', label='Dane')  # "Data"

    # Configure the right plot (measurements over time)
    ax2.scatter(listtestvalue[1], listtestvalue[0], color='g', s=2)
    ax2.set_title(f"Pomiary w czasie")  # "Measurements over time"
    ax2.set_xlabel(f"testy")  # "tests"
    ax2.set_ylabel("Wartosc testu")  # "Test value"
    ax2.tick_params(axis='x', rotation=20)

    # Prepare data for drawing tolerance lines on the time series plot
    chart_tolerance_draw = {}
    for j in range(len(listtestvalue[1])):
        chart_tolerance_draw[listtestvalue[1][j]] = tolerance_minus[j], tolerance_plus[j]

    # Sort tolerance data by timestamp
    posortowany_chart_tolerance_draw = dict(sorted(chart_tolerance_draw.items()))

    # Create a new dictionary with unique tolerance values associated with their first occurrence
    unique_chart_tolerance_draw = {}
    prev_date = None
    for key, value in posortowany_chart_tolerance_draw.items():
        if value != prev_date:
            unique_chart_tolerance_draw[key] = value
            prev_date = value

    prev_date = None
    # Get the first and last timestamps
    first_date = list(posortowany_chart_tolerance_draw.keys())[0]
    last_date = list(posortowany_chart_tolerance_draw.keys())[-1]

    prev_value = posortowany_chart_tolerance_draw[first_date]

    # Plot the tolerance lines as horizontal segments
    for key, value in unique_chart_tolerance_draw.items():
        if prev_date is None:
            prev_date = first_date

        prev_date = prev_date
        end_date = key

        ax2.plot([prev_date, end_date], [value[0], value[0]], color='red', linestyle='-', linewidth=1)  # Lower limit
        ax2.plot([prev_date, end_date], [value[1], value[1]], color='red', linestyle='-', linewidth=1)  # Upper limit

        prev_date = end_date
        prev_value = value

    # Plot the final segment of tolerance lines
    ax2.plot([prev_date, last_date], [value[0], value[0]], color='red', linestyle='-', linewidth=1)
    ax2.plot([prev_date, last_date], [value[1], value[1]], color='red', linestyle='-', linewidth=1)

    # Add grids to both plots
    ax1.grid(True)
    ax2.grid(True)

    # Show the plot
    plt.show()


def Chart_create_group(Dane_wejsciowe):
    # Turn on interactive mode for matplotlib
    plt.ion()

    # Helper functions for color brightness sorting
    def hex_to_rgb(hex_color):
        """Convert HEX color to RGB."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def brightness(rgb_color):
        """Calculate brightness of an RGB color."""
        r, g, b = rgb_color
        return 0.299 * r + 0.587 * g + 0.114 * b

    # Get a list of basic CSS4 colors and sort them by brightness
    colors_basic = list(mcolors.CSS4_COLORS.values())
    colors = sorted(colors_basic, key=lambda color: brightness(hex_to_rgb(color)))

    color_idx = 0  # (This variable is declared but not used in the loop below, 'i' is used instead)

    dicttestvalue = {}  # (This dictionary is declared but not used)

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Configure the left plot (histogram and normal distribution)
    ax1.set_xlabel('Wartosc')  # "Value"
    ax1.set_ylabel('Prawdopodobienstwo')  # "Probability"
    ax1.set_title('Rozklad danych i rozklad normalny')  # "Data distribution and normal distribution"
    ax1.grid(True)

    # Configure the right plot (measurements over time)
    ax2.set_title(f"Pomiary w czasie")  # "Measurements over time"
    ax2.set_xlabel(f"testy")  # "tests"
    ax2.set_ylabel("Wartosc testu")  # "Test value"
    ax2.tick_params(axis='x', rotation=20)

    # Add grids to both plots
    ax1.grid(True)
    ax2.grid(True)

    i = 0
    legend_elements = []
    # Iterate through each element in the input data dictionary
    for element_key in Dane_wejsciowe:
        i = i + 1
        # Parse input data for each group
        parts = Dane_wejsciowe[element_key][0]
        aux = Dane_wejsciowe[element_key][1]
        value = Dane_wejsciowe[element_key][2]
        boardsnumber = [float(x) for x in Dane_wejsciowe[element_key][3]]
        loc = Dane_wejsciowe[element_key][4]
        el = Dane_wejsciowe[element_key][5]
        reference = [float(x) for x in Dane_wejsciowe[element_key][6].replace('[', '').replace(']', '').split(',')]
        tolerance_plus = [float(x) for x in Dane_wejsciowe[element_key][7].replace('[', '').replace(']', '').split(',')]
        tolerance_minus = [float(x) for x in
                           Dane_wejsciowe[element_key][8].replace('[', '').replace(']', '').split(',')]

        # Process timestamp string to a list of datetime objects for each group
        Timestamp_list = Dane_wejsciowe[element_key][10].replace('[', '').replace(']', '').split("),")
        New_Timestamp_list = []

        for element in Timestamp_list:
            New_Timestamp_list.append(f"{element})")

        New_Timestamp_list_2 = []

        for date in New_Timestamp_list:
            try:
                try:
                    # Try parsing with microseconds
                    date_str = datetime.strptime(
                        date.replace(" ", "").replace("datetime.datetime", "").replace("(", "").replace(")", ""),
                        "%Y,%m,%d,%H,%M,%S,%f")
                except:
                    try:
                        # Try parsing without microseconds
                        date_str = datetime.strptime(
                            date.replace(" ", "").replace("datetime.datetime", "").replace("(", "").replace(")", ""),
                            "%Y,%m,%d,%H,%M,%S")
                    except:
                        # Try parsing with only minutes
                        date_str = datetime.strptime(
                            date.replace(" ", "").replace("datetime.datetime", "").replace("(", "").replace(")", ""),
                            "%Y,%m,%d,%H,%M")
                New_Timestamp_list_2.append(date_str)
                # print(f"{date_str}\n")
            except ValueError:
                print(f"Nieprawidlowy format daty -> {date}")  # "Invalid date format -> {date}"
            except Exception as e:
                print(f"Wystapil inny blad: {e}")  # "Another error occurred: {e}"

        # Combine test values and processed timestamps for each group
        listtestvalue = [float(x) for x in Dane_wejsciowe[element_key][9].replace('[', '').replace(']', '').split(
            ',')], New_Timestamp_list_2

        # Remove square brackets and split the string by commas
        string_list = Dane_wejsciowe[element_key][9].replace('[', '').replace(']', '').split(',')
        # Convert the list of strings to a list of floats (redundant as listtestvalue is already parsed)
        float_list = [float(x) for x in string_list]

        # Plot histogram of data for the current group
        ax1.hist(listtestvalue[0], bins=20, density=True, alpha=0.5, color='g', label='Dane')  # "Data"
        # Plot scatter data for the current group on the time series plot
        ax2.scatter(listtestvalue[1], listtestvalue[0], color=colors[i], s=2)

        # Adds element to legend for the current group
        legend_elements.append(
            Line2D([0], [0], marker='o', color='w', label=f'Grupa {i}', markerfacecolor=colors[i], markersize=10))

        # Prepare data for drawing tolerance lines on the time series plot for the current group
        chart_tolerance_draw = {}
        for j in range(len(listtestvalue[1])):
            chart_tolerance_draw[listtestvalue[1][j]] = tolerance_minus[j], tolerance_plus[j]

        # Sort tolerance data by timestamp
        posortowany_chart_tolerance_draw = dict(sorted(chart_tolerance_draw.items()))

        # Create a new dictionary with unique tolerance values associated with their first occurrence
        unique_chart_tolerance_draw = {}
        prev_date = None
        for key, value in posortowany_chart_tolerance_draw.items():
            if value != prev_date:
                unique_chart_tolerance_draw[key] = value
                prev_date = value

        prev_date = None
        # Get the first and last timestamps for the current group
        first_date = list(posortowany_chart_tolerance_draw.keys())[0]
        last_date = list(posortowany_chart_tolerance_draw.keys())[-1]

        prev_value = posortowany_chart_tolerance_draw[first_date]

        # Plot the tolerance lines as horizontal segments for the current group
        for key, value in unique_chart_tolerance_draw.items():
            if prev_date is None:
                prev_date = first_date

            prev_date = prev_date
            end_date = key

            ax2.plot([prev_date, end_date], [value[0], value[0]], color='red', linestyle='-',
                     linewidth=1)  # Lower limit
            ax2.plot([prev_date, end_date], [value[1], value[1]], color='red', linestyle='-',
                     linewidth=1)  # Upper limit

            prev_date = end_date
            prev_value = value

        # Plot the final segment of tolerance lines for the current group
        ax2.plot([prev_date, last_date], [value[0], value[0]], color='red', linestyle='-', linewidth=1)
        ax2.plot([prev_date, last_date], [value[1], value[1]], color='red', linestyle='-', linewidth=1)

    # Show legend on charts
    ax2.legend(handles=legend_elements, loc='center left', fontsize=7, bbox_to_anchor=(1, 0.5))

