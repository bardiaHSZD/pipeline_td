import tkinter as tk
from tkinter import ttk
from utils.function_utils import open_create_pipeline_window, open_register_shots_window, open_register_thumbnails_window, exit_program, show_about

# Colors
MENU_BAR_COLOR = "#232323"
MENU_COLOR = "#313234"
MENU_TEXT_COLOR = "#ffffff"
MENU_ACTIVE_COLOR = "#373c46"
PLAIN_BLACK = "#000000"

import tkinter as tk
from utils.function_utils import open_create_pipeline_window, open_register_shots_window, open_register_thumbnails_window, exit_program, show_about

def create_menu(root):
    """
    Creates the menu for the main app window and applies custom styles for dark mode.
    """
    # Create the menu bar with no borders and mimic shadow using background layers
    menu_bar = tk.Menu(root, bg=MENU_BAR_COLOR, fg=MENU_BAR_COLOR, activebackground=MENU_ACTIVE_COLOR, activeforeground=MENU_TEXT_COLOR,  activeborderwidth=0,border=0,borderwidth=0)

    # Add File menu
    file_menu = tk.Menu(menu_bar, tearoff=0, bg=MENU_BAR_COLOR, fg=MENU_TEXT_COLOR, activebackground=MENU_ACTIVE_COLOR, activeforeground=MENU_TEXT_COLOR, activeborderwidth=0,border=0,borderwidth=0)
    file_menu.add_command(label="Exit", command=lambda: exit_program(root))  # Pass root to exit_program
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Add Tools menu with submenus
    tools_menu = tk.Menu(menu_bar, tearoff=0, bg=MENU_BAR_COLOR, fg=MENU_TEXT_COLOR, activebackground=MENU_ACTIVE_COLOR, activeforeground=MENU_TEXT_COLOR,  activeborderwidth=0,border=0,borderwidth=0)
    tools_menu.add_command(label="Create Pipeline", command=lambda: open_create_pipeline_window(root))
    tools_menu.add_command(label="Register Shots", command=lambda: open_register_shots_window(root))
    tools_menu.add_command(label="Register Thumbnails", command=lambda: open_register_thumbnails_window(root))
    menu_bar.add_cascade(label="Tools", menu=tools_menu)

    # Add Help menu
    help_menu = tk.Menu(menu_bar, tearoff=0, bg=MENU_BAR_COLOR, fg=MENU_TEXT_COLOR, activebackground=MENU_ACTIVE_COLOR, activeforeground=MENU_TEXT_COLOR,  activeborderwidth=0,border=0,borderwidth=0)
    help_menu.add_command(label="About", command=show_about)
    menu_bar.add_cascade(label="Help", menu=help_menu)

    # Configure the menu for the root window
    root.config(menu=menu_bar)

    # Additional styling for shadow-like effect (layering)
    root.configure(bg="#2d3336")  # Main window background color
    root.option_add('*Menu.borderWidth', 0)  # Remove any border width
    root.option_add('*Menu*activeBorderWidth', 0)  # Remove active item border width


