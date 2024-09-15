import os
import shutil
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image  # Import PIL for image conversion

# Global variables to track the window instances
create_pipeline_window = None
register_shots_window = None
register_thumbnails_window = None
browse_window_open = False  # Variable to check if a browse window is already open

# Create Pipeline Window
def open_create_pipeline_window(root):
    global create_pipeline_window
    if create_pipeline_window is None or not tk.Toplevel.winfo_exists(create_pipeline_window):
        create_pipeline_window = tk.Toplevel(root)
        create_pipeline_window.title("Create Pipeline")
        create_pipeline_window.geometry("550x150")
        create_pipeline_window.resizable(False, False)  
        create_pipeline_window.transient(root)
        create_pipeline_window.attributes("-topmost", True)

        # Project Directory
        project_directory_label = tk.Label(create_pipeline_window, text="Project Directory:", anchor="e")
        project_directory_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        project_directory_entry = tk.Entry(create_pipeline_window, width=40)
        project_directory_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        browse_button_project = tk.Button(create_pipeline_window, text="Browse", 
                                          command=lambda: browse_project_directory(project_directory_entry, root))
        browse_button_project.grid(row=0, column=2, padx=10, pady=10)

        # Project Image
        project_image_label = tk.Label(create_pipeline_window, text="Project Image (.png):", anchor="e")
        project_image_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        project_image_entry = tk.Entry(create_pipeline_window, width=40)
        project_image_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        browse_button_image = tk.Button(create_pipeline_window, text="Browse", 
                                        command=lambda: browse_project_image(project_image_entry, root))
        browse_button_image.grid(row=1, column=2, padx=10, pady=10)

        # Generate Pipeline Button
        generate_pipeline_button = tk.Button(create_pipeline_window, text="Generate Pipeline", 
                                             command=lambda: generate_pipeline_action(create_pipeline_window, project_directory_entry, project_image_entry))
        generate_pipeline_button.grid(row=2, column=1, pady=10)

        create_pipeline_window.protocol("WM_DELETE_WINDOW", lambda: on_close(create_pipeline_window, 'pipeline'))
    else:
        create_pipeline_window.lift()

# Register Shots Window
def open_register_shots_window(root):
    global register_shots_window
    if register_shots_window is None or not tk.Toplevel.winfo_exists(register_shots_window):
        register_shots_window = tk.Toplevel(root)
        register_shots_window.title("Register Shots")
        register_shots_window.geometry("500x150")
        register_shots_window.resizable(False, False)
        register_shots_window.transient(root)
        register_shots_window.attributes("-topmost", True)

        # SHOTS folder selection
        shots_folder_label = tk.Label(register_shots_window, text="SHOTS Folder:", anchor="e")
        shots_folder_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        shots_folder_entry = tk.Entry(register_shots_window, width=40)
        shots_folder_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        browse_button_shots = tk.Button(register_shots_window, text="Browse", 
                                        command=lambda: browse_shots_folder(shots_folder_entry, root))
        browse_button_shots.grid(row=0, column=2, padx=10, pady=10)

        # Shotinfo save location
        save_path_label = tk.Label(register_shots_window, text="Shotinfo Location:", anchor="e")
        save_path_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        save_path_entry = tk.Entry(register_shots_window, width=40)
        save_path_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        browse_button_save = tk.Button(register_shots_window, text="Browse", 
                                       command=lambda: browse_save_location(save_path_entry, root))
        browse_button_save.grid(row=1, column=2, padx=10, pady=10)

        # Register Shots Button
        generate_button = tk.Button(register_shots_window, text="Register Now", 
                                    command=lambda: generate_json_action(register_shots_window, generate_button, shots_folder_entry, save_path_entry))
        generate_button.grid(row=2, column=1, pady=10)

        register_shots_window.protocol("WM_DELETE_WINDOW", lambda: on_close(register_shots_window, 'shots'))
    else:
        register_shots_window.lift()

# Register Thumbnails Window
def open_register_thumbnails_window(root):
    global register_thumbnails_window
    if register_thumbnails_window is None or not tk.Toplevel.winfo_exists(register_thumbnails_window):
        register_thumbnails_window = tk.Toplevel(root)
        register_thumbnails_window.title("Register Thumbnails")
        register_thumbnails_window.geometry("500x200")
        register_thumbnails_window.resizable(False, False)
        register_thumbnails_window.transient(root)
        register_thumbnails_window.attributes("-topmost", True)

        # Thumbnails File selection
        thumbnails_files_label = tk.Label(register_thumbnails_window, text="Thumbnails Files:", anchor="e")
        thumbnails_files_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        thumbnails_files_entry = tk.Entry(register_thumbnails_window, width=40)
        thumbnails_files_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        browse_button_thumbnails = tk.Button(register_thumbnails_window, text="Browse", 
                                             command=lambda: browse_thumbnails_files(thumbnails_files_entry, root))
        browse_button_thumbnails.grid(row=0, column=2, padx=10, pady=10)

        # Sequence Number Entry
        sequence_label = tk.Label(register_thumbnails_window, text="Sequence Number:", anchor="e")
        sequence_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        sequence_entry = tk.Entry(register_thumbnails_window, width=40)
        sequence_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Shotinfo Folder selection
        shotinfo_folder_label = tk.Label(register_thumbnails_window, text="Shotinfo Folder:", anchor="e")
        shotinfo_folder_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        shotinfo_folder_entry = tk.Entry(register_thumbnails_window, width=40)
        shotinfo_folder_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        browse_button_shotinfo = tk.Button(register_thumbnails_window, text="Browse", 
                                           command=lambda: browse_save_location(shotinfo_folder_entry, root))
        browse_button_shotinfo.grid(row=2, column=2, padx=10, pady=10)

        # Register Thumbnails Button
        register_thumbnails_button = tk.Button(register_thumbnails_window, text="Register Thumbnails", 
                                               command=lambda: register_thumbnails(sequence_entry, thumbnails_files_entry, shotinfo_folder_entry))
        register_thumbnails_button.grid(row=3, column=1, pady=10)

        register_thumbnails_window.protocol("WM_DELETE_WINDOW", lambda: on_close(register_thumbnails_window, 'thumbnails'))
    else:
        register_thumbnails_window.lift()

# Register Thumbnails Function
def register_thumbnails(sequence_entry, thumbnails_files_entry, shotinfo_folder_entry):
    thumbnails_files = thumbnails_files_entry.get().split(";")  # Split the files selected
    shotinfo_folder = shotinfo_folder_entry.get()
    seq = sequence_entry.get()

    if not thumbnails_files or not shotinfo_folder or not seq:
        messagebox.showerror("Error", "Please complete all fields.")
        return

    files = sorted([f for f in thumbnails_files if f.endswith(('.jpg', '.png'))])

    if not files:
        messagebox.showerror("Error", "No valid JPG or PNG files found in the selected files.")
        return

    common_prefix = os.path.commonprefix([os.path.basename(f) for f in files])

    for i, file in enumerate(files):
        shot_number = os.path.basename(file)[len(common_prefix):].split('.')[0]
        new_filename = f"seq_{seq.zfill(3)}-SH{i+1:03d}_preview.jpg"  # Output will always be .jpg

        # Convert and save the image as .jpg
        convert_to_jpg(file, os.path.join(shotinfo_folder, new_filename))

    messagebox.showinfo("Success", "Thumbnails registered successfully!")

# Utility function to convert any image to JPG
def convert_to_jpg(input_image_path, output_image_path):
    try:
        with Image.open(input_image_path) as img:
            rgb_img = img.convert('RGB')  # Convert image to RGB (necessary for JPG format)
            rgb_img.save(output_image_path, "JPEG")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert image {input_image_path} to JPG: {str(e)}")

# Utility Functions
def browse_project_directory(project_directory_entry, root):
    open_folder_dialog(project_directory_entry, root)

def browse_project_image(project_image_entry, root):
    global browse_window_open
    if not browse_window_open:
        browse_window_open = True
        image_path = filedialog.askopenfilename(title="Select Project Image (.png)", filetypes=[("PNG files", "*.png")], parent=root)
        if image_path:
            project_image_entry.delete(0, tk.END)
            project_image_entry.insert(0, image_path)
        browse_window_open = False

def browse_shots_folder(shots_folder_entry, root):
    open_folder_dialog(shots_folder_entry, root)

def browse_save_location(save_path_entry, root):
    open_folder_dialog(save_path_entry, root)

def browse_thumbnails_files(thumbnails_files_entry, root):
    """
    Browse for individual JPG and PNG files with multiple selection enabled.
    """
    global browse_window_open
    if not browse_window_open:
        browse_window_open = True
        files = filedialog.askopenfilenames(title="Select Thumbnails (.jpg, .png)", filetypes=[("Image files", "*.jpg *.png")], parent=root)
        if files:
            thumbnails_files_entry.delete(0, tk.END)
            thumbnails_files_entry.insert(0, ";".join(files))  # Store multiple paths separated by semicolons
        browse_window_open = False

def open_folder_dialog(entry_field, root):
    global browse_window_open
    if not browse_window_open:
        browse_window_open = True
        folder = filedialog.askdirectory(title="Select Folder", parent=root)
        if folder:
            entry_field.delete(0, tk.END)
            entry_field.insert(0, folder)
        browse_window_open = False

def on_close(window, window_type):
    global create_pipeline_window, register_shots_window, register_thumbnails_window, browse_window_open
    if window_type == 'pipeline':
        create_pipeline_window = None
    elif window_type == 'shots':
        register_shots_window = None
    elif window_type == 'thumbnails':
        register_thumbnails_window = None
    browse_window_open = False
    window.destroy()

def exit_program(root):
    root.quit()

def show_about():
    messagebox.showinfo("About", "Shot Info and Pipeline Generator - 2024")
