from PIL import Image
from tkinter import filedialog, messagebox
import tkinter as tk
import os


def browse_thumbnails_files(thumbnails_files_entry, root):
    files = filedialog.askopenfilenames(title="Select Thumbnails (.jpg, .png)", filetypes=[("Image files", "*.jpg *.png")], parent=root)
    if files:
        thumbnails_files_entry.delete(0, tk.END)
        thumbnails_files_entry.insert(0, " ".join(files))

def register_thumbnails(sequence_entry, shotinfo_folder_entry, thumbnails_files_entry):
    thumbnails_files = thumbnails_files_entry.get().split()
    sequence_number = sequence_entry.get()
    shotinfo_folder = shotinfo_folder_entry.get()

    if not thumbnails_files or not sequence_number or not shotinfo_folder:
        messagebox.showerror("Error", "Please select thumbnails, enter sequence number, and select shotinfo folder.")
        return

    thumbnails_files.sort()
    prefix = os.path.commonprefix(thumbnails_files)
    if not prefix:
        messagebox.showerror("Error", "Could not determine common prefix.")
        return

    for idx, filename in enumerate(thumbnails_files):
        shot_number = f"SH{str(idx + 1).zfill(5)}"
        destination_filename = f"seq_{sequence_number.zfill(5)}-{shot_number}_preview.jpg"
        destination_path = os.path.join(shotinfo_folder, destination_filename)

        if filename.endswith(".png") or filename.endswith(".jpg"):
            with Image.open(filename) as img:
                img.convert("RGB").save(destination_path, "JPEG")
        else:
            messagebox.showwarning("Warning", f"File {filename} is not a valid image format and was skipped.")
    
    messagebox.showinfo("Success", "Thumbnails have been registered successfully!")
