from tkinter import ttk

# Define the background color of the app
APP_BG_COLOR = "#2d3336"

# Apply dark theme to the app
def apply_dark_theme(root):
    style = ttk.Style()

    # Set theme to clam (supports dark mode)
    style.theme_use("clam")

    # Colors for dark mode
    dark_bg = APP_BG_COLOR
    light_text = "#ffffff"
    highlight_color = "#3b3b3b"
    button_hover_color = "#444444"
    selected_bg = "#4f535c"

    # Set window background
    root.configure(bg=dark_bg)

    # Configure the styles
    style.configure("TFrame", background=dark_bg)
    style.configure("TLabel", background=dark_bg, foreground=light_text)
    style.configure("TEntry", background=highlight_color, foreground=light_text, fieldbackground=dark_bg)
    style.configure("TButton", background=highlight_color, foreground=light_text, borderwidth=1)
    style.map("TButton", background=[('active', button_hover_color), ('pressed', selected_bg)])

    # Style combobox
    style.configure("TCombobox", background=dark_bg, foreground=light_text, fieldbackground=dark_bg)
    style.map("TCombobox", fieldbackground=[('readonly', dark_bg)], selectbackground=[('readonly', selected_bg)])

# Set the background color for new windows opened from submenus
def set_window_background(window):
    window.configure(bg=APP_BG_COLOR)
