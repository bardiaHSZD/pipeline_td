import os
import shutil
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image

# Global variables to track the window instances
create_pipeline_window = None
register_shots_window = None
register_thumbnails_window = None
browse_window_open = False  # Variable to check if a browse window is already open

# Define the background color of the app
APP_BG_COLOR = "#2d2d2d"

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

# Copy resources and prompt to overwrite if necessary
def copy_resources_with_confirm(source, destination):
    for item in os.listdir(source):
        s = os.path.join(source, item)
        d = os.path.join(destination, item)
        
        # Check if the destination file or folder already exists
        if os.path.exists(d):
            confirm = messagebox.askyesno("Overwrite Confirmation", f"'{item}' already exists in the destination folder. Do you want to overwrite it?")
            if not confirm:
                continue  # Skip copying this file or folder
        
        # Perform copy operation
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

# Modify pipeline.json to replace project name placeholder
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


# Function to generate pipeline and handle project directory and image processing
def generate_pipeline_action(window, project_directory_entry, project_image_entry):
    """
    This function performs the pipeline creation logic when the Generate Pipeline button is clicked.
    """
    project_path = project_directory_entry.get()
    project_image_path = project_image_entry.get()

    if not project_path:
        messagebox.showerror("Error", "Please select a project directory.")
        return

    project_name = os.path.basename(project_path)  # Extract project name from folder name
    pipeline_folder_path = os.path.join(project_path, '00_pipeline')
    cache_folder_path = os.path.join(project_path, 'cache')

    # Create folders if they don't exist
    for folder in [pipeline_folder_path, cache_folder_path]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Copy contents of "resources" folder into 00_pipeline folder
    app_dir = os.path.dirname(os.path.abspath(__file__))  # App directory
    resources_folder_path = os.path.join(app_dir, "resources")
    if os.path.exists(resources_folder_path):
        try:
            copy_resources_with_confirm(resources_folder_path, pipeline_folder_path)
            modify_pipeline_json(pipeline_folder_path, project_name)

            # Copy and rename the selected project image .png file to 'project.png'
            if project_image_path and os.path.exists(project_image_path):
                shutil.copy2(project_image_path, os.path.join(pipeline_folder_path, 'project.png'))
            else:
                messagebox.showwarning("Warning", "No valid project image selected. Skipping image copy.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create pipeline: {str(e)}")
    else:
        messagebox.showerror("Error", "Resources folder not found in app directory.")

    window.destroy()  # Close the window after pipeline creation

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
# Function to handle JSON generation for shots and close the window
def generate_json_action(window, button, shots_folder_entry, save_path_entry):
    """
    This function performs the action for generating the JSON for shots and closes the window upon success.
    """
    shots_folder = shots_folder_entry.get()
    save_path = save_path_entry.get()

    if not shots_folder or not save_path:
        messagebox.showerror("Error", "Please select both SHOTS folder and Save location.")
        return

    generate_shotinfo(shots_folder, save_path)  # Generate the shotinfo.json file
    window.destroy()  # Close the window on success

# Generate shotinfo.json based on the SHOTS folder
def generate_shotinfo(shots_folder, save_path):
    """
    Crawls the SHOTS folder to gather shot information and writes the data to shotinfo.json.
    """
    shot_ranges = {}
    start_frame = 1001  # Start frame for each shot

    for seq_folder in os.listdir(shots_folder):
        if seq_folder.startswith("seq_") and seq_folder[4:].isdigit():
            seq_path = os.path.join(shots_folder, seq_folder)
            if os.path.isdir(seq_path):
                shot_ranges[seq_folder] = {}
                for sh_folder in os.listdir(seq_path):
                    if sh_folder.startswith("SH") and sh_folder[2:].isdigit():
                        # Update path to find .nk file in Scenefiles/COMPOSITE/MAINCOMP
                        nk_path = os.path.join(seq_path, sh_folder, "Scenefiles", "COMPOSITE", "MAINCOMP")
                        end_frame = find_last_frame_in_nk_file(nk_path)  # Find end_frame from .nk file
                        shot_ranges[seq_folder][sh_folder] = [start_frame, end_frame]
    
    shotinfo = {"shotRanges": shot_ranges}

    # Write the shotinfo.json file
    with open(os.path.join(save_path, 'shotinfo.json'), 'w') as json_file:
        json.dump(shotinfo, json_file, indent=4)
    messagebox.showinfo("Success", "Shots registered successfully!")

# Find the last_frame value in the .nk file for determining end frame
def find_last_frame_in_nk_file(folder_path):
    """
    Search for the .nk file inside the folder and extract the last_frame value.
    """
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".nk"):
            nk_file_path = os.path.join(folder_path, file_name)
            with open(nk_file_path, 'r') as nk_file:
                for line in nk_file:
                    if 'last_frame' in line:
                        try:
                            return int(line.split()[1])  # Extract the frame number
                        except (IndexError, ValueError):
                            messagebox.showerror("Error", f"Invalid last_frame format in {nk_file_path}")
                            return 1100  # Default to 1100 if there's a parsing error
    return 1100  # Default if last_frame is not found

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

# Thumbnail registration logic
def register_thumbnails(sequence_entry, shotinfo_folder_entry, thumbnails_files_entry):
    thumbnails_files = thumbnails_files_entry.get().split()  # Split the string for multiple files
    sequence_number = sequence_entry.get()
    shotinfo_folder = shotinfo_folder_entry.get()

    if not thumbnails_files or not sequence_number or not shotinfo_folder:
        messagebox.showerror("Error", "Please select thumbnails, enter sequence number, and select shotinfo folder.")
        return

    thumbnails_files.sort()  # Sort the filenames

    # Find the longest common string from the beginning of the filenames
    prefix = os.path.commonprefix(thumbnails_files)
    if not prefix:
        messagebox.showerror("Error", "Could not determine common prefix.")
        return

    for idx, filename in enumerate(thumbnails_files):
        shot_number = f"SH{str(idx + 1).zfill(3)}"
        destination_filename = f"seq_{sequence_number.zfill(3)}-{shot_number}_preview.jpg"
        destination_path = os.path.join(shotinfo_folder, destination_filename)

        # Convert to JPG if necessary and save to destination
        if filename.endswith(".png") or filename.endswith(".jpg"):
            with Image.open(filename) as img:
                img.convert("RGB").save(destination_path, "JPEG")
        else:
            messagebox.showwarning("Warning", f"File {filename} is not a valid image format and was skipped.")

    messagebox.showinfo("Success", "Thumbnails have been registered successfully!")

# Browse project directory
def browse_project_directory(project_directory_entry, root):
    open_folder_dialog(project_directory_entry, root)

# Browse project image
def browse_project_image(project_image_entry, root):
    global browse_window_open
    if not browse_window_open:
        browse_window_open = True
        image_path = filedialog.askopenfilename(title="Select Project Image (.png)", filetypes=[("PNG files", "*.png")], parent=root)
        if image_path:
            project_image_entry.delete(0, tk.END)
            project_image_entry.insert(0, image_path)
        browse_window_open = False

# Browse thumbnails files
def browse_thumbnails_files(thumbnails_files_entry, root):
    global browse_window_open
    if not browse_window_open:
        browse_window_open = True
        files = filedialog.askopenfilenames(title="Select Thumbnails (.jpg, .png)", filetypes=[("Image files", "*.jpg *.png")], parent=root)
        if files:
            thumbnails_files_entry.delete(0, tk.END)
            thumbnails_files_entry.insert(0, " ".join(files))  # Join selected files into a string
        browse_window_open = False

# Browse SHOTS folder
def browse_shots_folder(shots_folder_entry, root):
    open_folder_dialog(shots_folder_entry, root)

# Browse save location
def browse_save_location(save_path_entry, root):
    open_folder_dialog(save_path_entry, root)

# Open folder dialog
def open_folder_dialog(entry_field, root):
    global browse_window_open
    if not browse_window_open:
        browse_window_open = True
        folder = filedialog.askdirectory(title="Select Folder", parent=root)
        if folder:
            entry_field.delete(0, tk.END)
            entry_field.insert(0, folder)
        browse_window_open = False

# Exit program
def exit_program(root):
    root.quit()

# About
def show_about():
    messagebox.showinfo("About", "Copyright EEFA FX 2024")
