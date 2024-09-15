import os
import shutil
from tkinter import filedialog, messagebox
from utils.theme_utils import APP_BG_COLOR
import tkinter as tk

browse_window_open = False

def browse_project_image(project_image_entry, root):
    global browse_window_open
    if not browse_window_open:
        browse_window_open = True
        image_path = filedialog.askopenfilename(title="Select Project Image (.png)", filetypes=[("PNG files", "*.png")], parent=root)
        if image_path:
            project_image_entry.delete(0, tk.END)
            project_image_entry.insert(0, image_path)
        browse_window_open = False

def copy_resources_with_confirm(source, destination):
    for item in os.listdir(source):
        s = os.path.join(source, item)
        d = os.path.join(destination, item)

        if os.path.exists(d):
            confirm = messagebox.askyesno("Overwrite Confirmation", f"'{item}' already exists in the destination folder. Do you want to overwrite it?")
            if not confirm:
                continue  # Skip copying this file or folder

        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

def modify_pipeline_json(pipeline_folder, project_name):
    pipeline_json_path = os.path.join(pipeline_folder, 'pipeline.json')
    if os.path.exists(pipeline_json_path):
        with open(pipeline_json_path, 'r') as file:
            content = file.read()
        modified_content = content.replace("{{PROJECT_NAME}}", f'"{project_name}"')
        with open(pipeline_json_path, 'w') as file:
            file.write(modified_content)
        messagebox.showinfo("Success", f"Pipeline initialized successfully.")
    else:
        messagebox.showerror("Error", "pipeline.json not found in the resources folder.")
        
def browse_project_directory(project_directory_entry, root):
    folder = filedialog.askdirectory(title="Select Project Directory", parent=root)
    if folder:
        project_directory_entry.delete(0, tk.END)
        project_directory_entry.insert(0, folder)

def generate_pipeline_action(window, project_directory_entry, project_image_entry):
    project_path = project_directory_entry.get()
    project_image_path = project_image_entry.get()

    if not project_path:
        messagebox.showerror("Error", "Please select a project directory.")
        return

    project_name = os.path.basename(project_path)
    pipeline_folder_path = os.path.join(project_path, '00_pipeline')
    cache_folder_path = os.path.join(project_path, 'cache')

    for folder in [pipeline_folder_path, cache_folder_path]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    app_dir = os.path.dirname(os.path.abspath(__file__))
    resources_folder_path = os.path.join(app_dir, "resources")
    if os.path.exists(resources_folder_path):
        try:
            copy_resources_with_confirm(resources_folder_path, pipeline_folder_path)
            modify_pipeline_json(pipeline_folder_path, project_name)

            if project_image_path and os.path.exists(project_image_path):
                shutil.copy2(project_image_path, os.path.join(pipeline_folder_path, 'project.png'))
            else:
                messagebox.showwarning("Warning", "No valid project image selected. Skipping image copy.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create pipeline: {str(e)}")
    else:
        messagebox.showerror("Error", "Resources folder not found in app directory.")
    window.destroy()

def browse_shots_folder(shots_folder_entry, root):
    folder = filedialog.askdirectory(title="Select SHOTS Folder", parent=root)
    if folder:
        shots_folder_entry.delete(0, tk.END)
        shots_folder_entry.insert(0, folder)

def browse_save_location(save_path_entry, root):
    folder = filedialog.askdirectory(title="Select Save Location", parent=root)
    if folder:
        save_path_entry.delete(0, tk.END)
        save_path_entry.insert(0, folder)
