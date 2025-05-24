# -*- coding: utf-8 -*-

# My custom classes

class Wyrob:
    # Constructor for the Wyrob (Product) class
    def __init__(self, masterid, Panel_Serial_number, boardsnumber, parts, aux, value, loc, el, reference,
                 tolerance_plus, tolerance_minus, timestamp, testvalue, proces):
        self.masterid = masterid  # Unique identifier for the product
        self.Panel_Serial_number = Panel_Serial_number  # Combined panel or serial number
        self.boardsnumber = boardsnumber  # Number of boards in the panel/product
        self.parts = parts  # Part number or component name
        self.aux = aux  # Auxiliary information (e.g., specific test point)
        self.value = value  # Nominal value of the tested parameter
        self.loc = loc  # Location on the board (e.g., component designator)
        self.el = el  # Element type (e.g., resistor, capacitor)
        self.reference = reference  # Reference value for the test
        self.tolerance_plus = tolerance_plus  # Upper tolerance limit
        self.tolerance_minus = tolerance_minus  # Lower tolerance limit
        self.testvalue = testvalue  # Actual measured test value
        self.proces = proces  # Testing process (e.g., FPT, ICT, FFT)
        self.timestamp = timestamp  # Timestamp of the test


class Testy_wyrobow:
    # Constructor for the Testy_wyrobow (Product Tests) class
    def __init__(self, parts, aux, value, boardsnumber, loc, el, reference, tolerance_plus, tolerance_minus, testvalue,
                 timestamp):
        self.parts = parts  # Part number or component name
        self.aux = aux  # Auxiliary information
        self.value = value  # Nominal value
        self.boardsnumber = boardsnumber  # Number of boards
        self.loc = loc  # Location on the board
        self.el = el  # Element type
        self.reference = (reference)  # Reference value (stored as a list)
        self.tolerance_plus = (tolerance_plus)  # Upper tolerance limit (stored as a list)
        self.tolerance_minus = (tolerance_minus)  # Lower tolerance limit (stored as a list)
        self.listtestvalue = [(testvalue), (timestamp)]  # List containing test values and timestamps


class Wyniki_testow:
    # Constructor for the Wyniki_testow (Test Results) class
    def __init__(self, fixture, testname, group, cp, cpk, pp, ppk, o_stand, limitchange):
        self.fixture = fixture,  # Test fixture ID
        self.testname = testname,  # Name of the test
        self.group = group,  # Group identifier
        self.cp = cp,  # Process Capability (Cp)
        self.cpk = cpk,  # Process Capability Index (Cpk)
        self.pp = pp,  # Process Performance (Pp)
        self.ppk = ppk,  # Process Performance Index (Ppk)
        self.o_stand = o_stand  # Standard deviation
        self.limitchange = limitchange  # Indicates if limits have changed

