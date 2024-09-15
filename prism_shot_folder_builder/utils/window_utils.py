import tkinter as tk
from tkinter import ttk
from utils.file_operations import browse_project_directory, browse_shots_folder, browse_save_location
from utils.theme_utils import set_window_background
from utils.json_operations import generate_json_action
from utils.file_operations import generate_pipeline_action
from utils.image_utils import register_thumbnails, browse_thumbnails_files
from utils.file_operations import browse_project_image

# Global variables to track the window instances
create_pipeline_window = None
register_shots_window = None
register_thumbnails_window = None

# Handle window close actions
def on_close(window, window_type):
    global create_pipeline_window, register_shots_window, register_thumbnails_window
    if window_type == 'pipeline':
        create_pipeline_window = None
    elif window_type == 'shots':
        register_shots_window = None
    elif window_type == 'thumbnails':
        register_thumbnails_window = None
    window.destroy()

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

        # Set background for the window
        set_window_background(create_pipeline_window)

        # Project Directory
        project_directory_label = ttk.Label(create_pipeline_window, text="Project Directory:")
        project_directory_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        project_directory_entry = ttk.Entry(create_pipeline_window, width=40)
        project_directory_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        browse_button_project = ttk.Button(create_pipeline_window, text="Browse", 
                                           command=lambda: browse_project_directory(project_directory_entry, root))
        browse_button_project.grid(row=0, column=2, padx=10, pady=10)

        # Project Image
        project_image_label = ttk.Label(create_pipeline_window, text="Project Image (.png):")
        project_image_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        project_image_entry = ttk.Entry(create_pipeline_window, width=40)
        project_image_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        browse_button_image = ttk.Button(create_pipeline_window, text="Browse", 
                                         command=lambda: browse_project_image(project_image_entry, root))
        browse_button_image.grid(row=1, column=2, padx=10, pady=10)

        # Generate Pipeline Button
        generate_pipeline_button = ttk.Button(create_pipeline_window, text="Generate Pipeline", 
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
        register_shots_window.geometry("550x150")
        register_shots_window.resizable(False, False)
        register_shots_window.transient(root)
        register_shots_window.attributes("-topmost", True)

        # Set background for the window
        set_window_background(register_shots_window)

        # SHOTS folder selection
        shots_folder_label = ttk.Label(register_shots_window, text="SHOTS Folder:")
        shots_folder_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        shots_folder_entry = ttk.Entry(register_shots_window, width=40)
        shots_folder_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        browse_button_shots = ttk.Button(register_shots_window, text="Browse", 
                                         command=lambda: browse_shots_folder(shots_folder_entry, root))
        browse_button_shots.grid(row=0, column=2, padx=10, pady=10)

        # Shotinfo save location
        save_path_label = ttk.Label(register_shots_window, text="Shotinfo Location:")
        save_path_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        save_path_entry = ttk.Entry(register_shots_window, width=40)
        save_path_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        browse_button_save = ttk.Button(register_shots_window, text="Browse", 
                                        command=lambda: browse_save_location(save_path_entry, root))
        browse_button_save.grid(row=1, column=2, padx=10, pady=10)

        # Register Shots Button
        generate_button = ttk.Button(register_shots_window, text="Register Now", 
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
        register_thumbnails_window.geometry("550x200")
        register_thumbnails_window.resizable(False, False)
        register_thumbnails_window.transient(root)
        register_thumbnails_window.attributes("-topmost", True)

        # Set background for the window
        set_window_background(register_thumbnails_window)

        # Thumbnails File selection
        thumbnails_files_label = ttk.Label(register_thumbnails_window, text="Thumbnails Files (.jpg, .png):")
        thumbnails_files_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        thumbnails_files_entry = ttk.Entry(register_thumbnails_window, width=40)
        thumbnails_files_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        browse_button_thumbnails = ttk.Button(register_thumbnails_window, text="Browse", 
                                              command=lambda: browse_thumbnails_files(thumbnails_files_entry, root))
        browse_button_thumbnails.grid(row=0, column=2, padx=10, pady=10)

        # Sequence Number Entry
        sequence_label = ttk.Label(register_thumbnails_window, text="Sequence Number:")
        sequence_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        sequence_entry = ttk.Entry(register_thumbnails_window, width=40)
        sequence_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Shotinfo Folder selection
        shotinfo_folder_label = ttk.Label(register_thumbnails_window, text="Shotinfo Folder:")
        shotinfo_folder_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        shotinfo_folder_entry = ttk.Entry(register_thumbnails_window, width=40)
        shotinfo_folder_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        browse_button_shotinfo = ttk.Button(register_thumbnails_window, text="Browse", 
                                            command=lambda: browse_save_location(shotinfo_folder_entry, root))
        browse_button_shotinfo.grid(row=2, column=2, padx=10, pady=10)

        # Register Thumbnails Button
        register_thumbnails_button = ttk.Button(register_thumbnails_window, text="Register Thumbnails", 
                                                command=lambda: register_thumbnails(sequence_entry, shotinfo_folder_entry, thumbnails_files_entry))
        register_thumbnails_button.grid(row=3, column=1, pady=10)

        register_thumbnails_window.protocol("WM_DELETE_WINDOW", lambda: on_close(register_thumbnails_window, 'thumbnails'))
    else:
        register_thumbnails_window.lift()
