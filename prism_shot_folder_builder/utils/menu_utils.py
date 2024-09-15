import tkinter as tk
from utils.window_utils import open_create_pipeline_window, open_register_shots_window, open_register_thumbnails_window
from utils.helpers import show_about, exit_program

def create_menu(root):
    menu_bar = tk.Menu(root)

    # Add File menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Exit", command=lambda: exit_program(root))
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Add Tools menu with submenus
    tools_menu = tk.Menu(menu_bar, tearoff=0)
    tools_menu.add_command(label="Create Pipeline", command=lambda: open_create_pipeline_window(root))
    tools_menu.add_command(label="Register Shots", command=lambda: open_register_shots_window(root))
    tools_menu.add_command(label="Register Thumbnails", command=lambda: open_register_thumbnails_window(root))
    menu_bar.add_cascade(label="Tools", menu=tools_menu)

    # Add Help menu
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About", command=show_about)
    menu_bar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menu_bar)
