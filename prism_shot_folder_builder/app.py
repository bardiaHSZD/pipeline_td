import tkinter as tk
from utils.menu_utils import create_menu
from utils.function_utils import exit_program, show_about  # Import the required functions

# Create the main window
root = tk.Tk()
root.title("Shot Info and Pipeline Generator")
root.geometry("1024x768")  # Set initial size
root.state('normal')  # Enable maximize functionality

# Create the menu bar and add it to the root window
create_menu(root)

# Start the GUI loop
root.mainloop()

