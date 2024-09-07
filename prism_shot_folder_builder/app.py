import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to crawl the SHOTS folder and generate the shotinfo.json
def generate_shotinfo(shots_folder, save_path):
    shot_ranges = {}
    for seq_folder in os.listdir(shots_folder):
        if seq_folder.startswith("seq_") and seq_folder[4:].isdigit():
            seq_path = os.path.join(shots_folder, seq_folder)
            if os.path.isdir(seq_path):
                shot_ranges[seq_folder] = {}
                for sh_folder in os.listdir(seq_path):
                    if sh_folder.startswith("SH") and sh_folder[2:].isdigit():
                        shot_ranges[seq_folder][sh_folder] = [1001, 1100]
    
    shotinfo = {"shotRanges": shot_ranges}

    with open(os.path.join(save_path, 'shotinfo.json'), 'w') as json_file:
        json.dump(shotinfo, json_file, indent=4)
    messagebox.showinfo("Success", "shotinfo.json file created successfully.")

# Function to browse for SHOTS folder
def browse_shots_folder():
    shots_folder = filedialog.askdirectory(title="Select SHOTS Folder")
    if shots_folder:
        shots_folder_entry.delete(0, tk.END)
        shots_folder_entry.insert(0, shots_folder)

# Function to browse where to save the JSON file
def browse_save_location():
    save_path = filedialog.askdirectory(title="Select Folder to Save JSON")
    if save_path:
        save_path_entry.delete(0, tk.END)
        save_path_entry.insert(0, save_path)

# Function to handle the Generate button click
def on_generate_click():
    shots_folder = shots_folder_entry.get()
    save_path = save_path_entry.get()

    if not shots_folder or not save_path:
        messagebox.showerror("Error", "Please select both SHOTS folder and Save location.")
        return

    generate_shotinfo(shots_folder, save_path)

# Function for the Exit submenu
def exit_program():
    root.quit()

# Function for the About submenu
def show_about():
    messagebox.showinfo("About", "Copyright EEFA FX 2024")

# Create the main window
root = tk.Tk()
root.title("Shot Info Generator")
root.geometry("450x250")
root.resizable(False, False)

# Create the menu bar
menu_bar = tk.Menu(root)

# Add File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=exit_program)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

# Create the widgets for SHOTS folder selection
shots_folder_label = tk.Label(root, text="SHOTS Folder:")
shots_folder_label.pack(pady=5)
shots_folder_entry = tk.Entry(root, width=40)
shots_folder_entry.pack(pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_shots_folder)
browse_button.pack(pady=5)

# Create the widgets for save location selection
save_path_label = tk.Label(root, text="Save Location:")
save_path_label.pack(pady=5)
save_path_entry = tk.Entry(root, width=40)
save_path_entry.pack(pady=5)
save_button = tk.Button(root, text="Browse", command=browse_save_location)
save_button.pack(pady=5)

# Create the Generate button and ensure it's at the bottom
generate_button = tk.Button(root, text="Generate JSON", command=on_generate_click)
generate_button.pack(pady=20)

# Start the GUI loop
root.mainloop()
