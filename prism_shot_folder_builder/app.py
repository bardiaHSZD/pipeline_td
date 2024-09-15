import tkinter as tk
from utils.menu_utils import create_menu
from utils.helpers import exit_program, show_about
from utils.theme_utils import apply_dark_theme

# Create the main window
root = tk.Tk()
root.title("Shot Info and Pipeline Generator")
root.geometry("1024x768")

# Apply dark theme to the app
apply_dark_theme(root)

# Create the menu bar and add it to the root window
create_menu(root)

# Start the GUI loop
root.mainloop()
