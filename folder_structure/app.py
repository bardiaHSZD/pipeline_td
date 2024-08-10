import tkinter as tk
from tkinter import filedialog, messagebox, Menu
import json
import os

def browse_json():
    file_path = filedialog.askopenfilename(
        title="Select JSON File",
        filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
    )
    json_entry.delete(0, tk.END)
    json_entry.insert(0, file_path)

def browse_folder():
    folder_path = filedialog.askdirectory(title="Select Destination Folder")
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def create_folders():
    json_path = json_entry.get()
    destination_path = folder_entry.get()

    if not json_path or not destination_path:
        messagebox.showerror("Error", "Both JSON file and destination folder must be selected.")
        return

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        def create_subfolders(base_path, subcategories):
            for subcategory in subcategories:
                if isinstance(subcategory, dict):
                    subcategory_name = subcategory.get("subcategory", "")
                    subcategory_path = os.path.join(base_path, subcategory_name)
                    os.makedirs(subcategory_path, exist_ok=True)
                    
                    # Recursively create sub-subcategories if they exist
                    if "sub_subcategories" in subcategory:
                        create_subfolders(subcategory_path, subcategory["sub_subcategories"])
                elif isinstance(subcategory, str):
                    subcategory_path = os.path.join(base_path, subcategory)
                    os.makedirs(subcategory_path, exist_ok=True)

        for collection in data.get("collections", []):
            category_name = collection.get("category", "")
            if category_name:
                category_path = os.path.join(destination_path, category_name)
                os.makedirs(category_path, exist_ok=True)

                create_subfolders(category_path, collection.get("subcategories", []))

        messagebox.showinfo("Success", "Folder hierarchy created successfully!")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Failed to parse JSON. Please check the JSON file for errors.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def show_about():
    messagebox.showinfo("About", "Copyright 2024 EEFA FX")

# Set up the main application window
app = tk.Tk()
app.title("JSON Folder Creator")

# Set a fixed window size
app.geometry("500x250")
app.resizable(False, False)

# Create a menu bar
menu_bar = Menu(app)

# Create Help menu
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Add the menu bar to the app
app.config(menu=menu_bar)

# JSON file selection
json_label = tk.Label(app, text="Select JSON File:")
json_label.pack(pady=5, anchor="w", padx=10)
json_entry = tk.Entry(app, width=50)
json_entry.pack(padx=10, pady=5)
json_button = tk.Button(app, text="Browse", command=browse_json)
json_button.pack(pady=5)

# Destination folder selection
folder_label = tk.Label(app, text="Select Destination Folder:")
folder_label.pack(pady=5, anchor="w", padx=10)
folder_entry = tk.Entry(app, width=50)
folder_entry.pack(padx=10, pady=5)
folder_button = tk.Button(app, text="Browse", command=browse_folder)
folder_button.pack(pady=5)

# Apply button
apply_button = tk.Button(app, text="Apply", command=create_folders)
apply_button.pack(pady=20)

# Run the application
app.mainloop()
