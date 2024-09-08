import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # For separator line

# Function to browse for project folder
def browse_project_directory():
    project_directory = filedialog.askdirectory(title="Select Project Directory")
    if project_directory:
        project_directory_entry.delete(0, tk.END)
        project_directory_entry.insert(0, project_directory)

# Function to create the 00_pipeline folder and generate pipeline
def create_pipeline():
    project_path = project_directory_entry.get()
    if not project_path:
        messagebox.showerror("Error", "Please select a project directory.")
        return
    
    project_name = os.path.basename(project_path)  # Extract project name from folder name
    pipeline_folder_path = os.path.join(project_path, '00_pipeline')
    
    # Create 00_pipeline folder if it does not exist
    if not os.path.exists(pipeline_folder_path):
        os.makedirs(pipeline_folder_path)

    # Copy contents of "resources" folder into 00_pipeline folder
    app_dir = os.path.dirname(os.path.abspath(__file__))  # App directory
    resources_folder_path = os.path.join(app_dir, "resources")
    if os.path.exists(resources_folder_path):
        try:
            copy_resources_with_confirm(resources_folder_path, pipeline_folder_path)
            modify_pipeline_json(pipeline_folder_path, project_name)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create pipeline: {str(e)}")
    else:
        messagebox.showerror("Error", "Resources folder not found in app directory.")

# Function to copy resources into 00_pipeline folder with confirmation for overwriting files
def copy_resources_with_confirm(source, destination):
    for item in os.listdir(source):
        s = os.path.join(source, item)
        d = os.path.join(destination, item)
        
        # Check if the destination file or folder already exists
        if os.path.exists(d):
            # Ask for confirmation to overwrite the file
            confirm = messagebox.askyesno("Overwrite Confirmation", f"'{item}' already exists in the destination folder. Do you want to overwrite it?")
            if not confirm:
                continue  # Skip copying this file or folder
        
        # Perform copy operation
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

# Function to modify the pipeline.json file
def modify_pipeline_json(pipeline_folder, project_name):
    pipeline_json_path = os.path.join(pipeline_folder, 'pipeline.json')
    if os.path.exists(pipeline_json_path):
        # Read the existing json file
        with open(pipeline_json_path, 'r') as file:
            content = file.read()

        # Replace placeholder with project name in quotes
        modified_content = content.replace("{{PROJECT_NAME}}", f'"{project_name}"')

        # Save the modified file
        with open(pipeline_json_path, 'w') as file:
            file.write(modified_content)

        messagebox.showinfo("Success", f"Pipeline folder and JSON file created successfully with project name '{project_name}'.")
    else:
        messagebox.showerror("Error", "pipeline.json not found in the resources folder.")

# Function to browse for SHOTS folder and generate shotinfo.json
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
root.title("Shot Info and Pipeline Generator")
root.geometry("500x350")
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

# Create the Project Directory section
project_directory_frame = tk.Frame(root)
project_directory_frame.pack(pady=10, padx=20, fill='x')

project_directory_label = tk.Label(project_directory_frame, text="Project Directory:")
project_directory_label.pack(side='left', padx=5)
project_directory_entry = tk.Entry(project_directory_frame, width=40)
project_directory_entry.pack(side='left', padx=5)
browse_button_project = tk.Button(project_directory_frame, text="Browse", command=browse_project_directory)
browse_button_project.pack(side='left', padx=5)

# Create the Generate Pipeline button
generate_pipeline_button = tk.Button(root, text="Generate Pipeline", command=create_pipeline)
generate_pipeline_button.pack(pady=10)

# Add a separator line
separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x', pady=10)

# Create a frame for SHOTS folder selection
shots_folder_frame = tk.Frame(root)
shots_folder_frame.pack(pady=5, padx=20, fill='x')

shots_folder_label = tk.Label(shots_folder_frame, text="SHOTS Folder:")
shots_folder_label.pack(side='left', padx=5)
shots_folder_entry = tk.Entry(shots_folder_frame, width=40)
shots_folder_entry.pack(side='left', padx=5)
browse_button_shots = tk.Button(shots_folder_frame, text="Browse", command=browse_shots_folder)
browse_button_shots.pack(side='left', padx=5)

# Create a frame for save location selection
save_path_frame = tk.Frame(root)
save_path_frame.pack(pady=5, padx=20, fill='x')

save_path_label = tk.Label(save_path_frame, text="Save Location:")
save_path_label.pack(side='left', padx=5)
save_path_entry = tk.Entry(save_path_frame, width=40)
save_path_entry.pack(side='left', padx=5)
browse_button_save = tk.Button(save_path_frame, text="Browse", command=browse_save_location)
browse_button_save.pack(side='left', padx=5)

# Create the Generate JSON button
generate_button = tk.Button(root, text="Generate JSON", command=on_generate_click)
generate_button.pack(pady=10)

# Start the GUI loop
root.mainloop()
