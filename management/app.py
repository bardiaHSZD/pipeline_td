import os
import json
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# Load JSON data
def load_json_data(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

# Load data from Excel
def load_excel_data(excel_file):
    project_data = {}
    
    # Load the ProjectInfo sheet
    project_info = pd.read_excel(excel_file, sheet_name='ProjectInfo')
    project_name = project_info['project_name'].iloc[0]
    project_data['project_name'] = project_name

    # Load the Entities sheet
    entities = pd.read_excel(excel_file, sheet_name='Entities')
    entity_dict = {}
    for entity in entities['entity_name'].unique():
        entity_tasks = entities[entities['entity_name'] == entity]
        entity_dict[entity] = {}
        for _, row in entity_tasks.iterrows():
            department = row['department']
            task = row['task']
            if department not in entity_dict[entity]:
                entity_dict[entity][department] = []
            entity_dict[entity][department].append(task)
    project_data['entities'] = entity_dict

    # Load the Sequences sheet
    sequences = pd.read_excel(excel_file, sheet_name='Sequences')
    sequence_dict = {}
    for sequence in sequences['sequence_name'].unique():
        sequence_dict[sequence] = {'shots': {}}
        sequence_shots = sequences[sequences['sequence_name'] == sequence]
        for shot in sequence_shots['shot_name'].unique():
            sequence_dict[sequence]['shots'][shot] = {}
            shot_tasks = sequence_shots[sequence_shots['shot_name'] == shot]
            for _, row in shot_tasks.iterrows():
                department = row['department']
                task = row['task']
                if department not in sequence_dict[sequence]['shots'][shot]:
                    sequence_dict[sequence]['shots'][shot][department] = []
                sequence_dict[sequence]['shots'][shot][department].append(task)
    project_data['sequences'] = sequence_dict

    return project_data

# Create structure for each entity based on its specific task data
def create_entity_structure(entity_name, asset_tasks):
    return {
        "Exports": {},
        "Playblasts": {},
        "Renders": {},
        "Scenefiles": {
            department: {
                task: {} for task in tasks
            } for department, tasks in asset_tasks.items()
        }
    }

# Create structure for each shot based on its specific task data
def create_shot_structure(shot_tasks):
    return {
        "Exports": {},
        "Playblasts": {},
        "Renders": {},
        "Scenefiles": {
            department: {
                task: {} for task in tasks
            } for department, tasks in shot_tasks.items()
        }
    }

# Define the folder structure based on the data
def create_folder_structure(project_data):
    project_name = project_data['project_name']
    entities = project_data.get('entities', {})
    sequences = project_data.get('sequences', {})

    folder_structure = {
        project_name: {
            "Production": {
                "Assets": {
                    "Entities": {
                        entity: create_entity_structure(entity, tasks)
                        for entity, tasks in entities.items()
                    }
                },
                "Shots": {
                    sequence: {
                        shot: create_shot_structure(shot_tasks)
                        for shot, shot_tasks in sequence_data['shots'].items()
                    } for sequence, sequence_data in sequences.items()
                }
            },
            "Pipeline": {},
            "Cache": {}
        }
    }

    return folder_structure

# Function to create folders recursively
def create_folders(structure, base_path=""):
    for key, value in structure.items():
        full_path = os.path.join(base_path, key)
        os.makedirs(full_path, exist_ok=True)
        print(f"Created directory: {full_path}")
        if isinstance(value, dict):
            create_folders(value, full_path)

# Function to handle file browsing
def browse_file():
    if var.get() == "json":
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    elif var.get() == "excel":
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    else:
        file_path = ""
    
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

# Function to apply the file choice and create the structure
def apply_selection():
    file_path = entry_file_path.get()
    if not file_path:
        messagebox.showerror("Error", "No file selected")
        return

    if var.get() == "json":
        project_data = load_json_data(file_path)
    elif var.get() == "excel":
        project_data = load_excel_data(file_path)
    else:
        messagebox.showerror("Error", "Invalid selection")
        return

    folder_structure = create_folder_structure(project_data)
    create_folders(folder_structure)

    messagebox.showinfo("Success", "Folder structure created successfully")

# Function for the About dialog
def show_about():
    messagebox.showinfo("About", "Copyright 2024")

# Setting up the GUI
root = tk.Tk()
root.title("Project Structure Generator")
root.geometry("400x220")  # Fixed window size
root.resizable(False, False)  # Disable resizing

# Menu bar with Help -> About
menu_bar = tk.Menu(root)
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menu_bar)

var = tk.StringVar(value="json")

tk.Label(root, text="Select the input file type:").pack(pady=10)

# Radio buttons for file selection
tk.Radiobutton(root, text="JSON File", variable=var, value="json").pack(anchor=tk.W, padx=20)
tk.Radiobutton(root, text="Excel File", variable=var, value="excel").pack(anchor=tk.W, padx=20)

# Entry for file path
entry_file_path = tk.Entry(root, width=50)
entry_file_path.pack(pady=10)

# Browse button
tk.Button(root, text="Browse", command=browse_file).pack(pady=5)

# Apply button
tk.Button(root, text="Apply", command=apply_selection).pack(pady=10)

# Run the GUI event loop
root.mainloop()
