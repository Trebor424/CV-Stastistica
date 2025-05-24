# -*- coding: utf-8 -*-

import tkinter as tk
import Form1_MainForm

if __name__ == "__main__":
    # Create the main Tkinter window
    Mainform_screen = tk.Tk()
    # Create an instance of MainForm
    main_form = Form1_MainForm.MainForm(Mainform_screen)
    # Start the Tkinter event loop
    Mainform_screen.mainloop()