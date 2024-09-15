import tkinter as tk
from utils.menu_utils import create_menu
from utils.function_utils import apply_dark_theme, exit_program, show_about

# Create the main window
root = tk.Tk()
root.title("Shot Info and Pipeline Generator")
root.geometry("1024x768")  # Set initial size
root.state('normal')  # Enable maximize functionality

# Apply dark theme
apply_dark_theme(root)

# Create the menu bar and add it to the root window
create_menu(root)

# Start the GUI loop
root.mainloop()
