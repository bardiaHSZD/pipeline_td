from PIL import Image
from tkinter import filedialog, messagebox
import tkinter as tk
import os
from natsort import natsorted  # Import natsort for natural sorting


def browse_thumbnails_files(thumbnails_files_entry, root):
    files = filedialog.askopenfilenames(title="Select Thumbnails (.jpg, .png)", filetypes=[("Image files", "*.jpg *.png")], parent=root)
    if files:
        # Properly join the filenames by enclosing them in double quotes to handle spaces
        thumbnails_files_entry.delete(0, tk.END)
        thumbnails_files_entry.insert(0, " ".join(f'"{file}"' for file in files))


# Thumbnail registration logic with natural sorting
def register_thumbnails(sequence_entry, shotinfo_folder_entry, thumbnails_files_entry):
    thumbnails_files = thumbnails_files_entry.get().split()  # Split the string for multiple files
    sequence_number = sequence_entry.get()
    shotinfo_folder = shotinfo_folder_entry.get()

    if not thumbnails_files or not sequence_number or not shotinfo_folder:
        messagebox.showerror("Error", "Please select thumbnails, enter sequence number, and select shotinfo folder.")
        return

    # Remove any surrounding quotes from filenames
    thumbnails_files = [file.strip('"') for file in thumbnails_files]

    # Sort filenames naturally (as in Windows)
    thumbnails_files = natsorted(thumbnails_files)

    for idx, filename in enumerate(thumbnails_files):
        shot_number = f"SH{str(idx + 1).zfill(5)}"  # 5 digits for shot numbering
        destination_filename = f"seq_{sequence_number.zfill(5)}-{shot_number}_preview.jpg"
        destination_path = os.path.join(shotinfo_folder, destination_filename)

        # Check if the file is JPEG, and if not, convert it
        try:
            with Image.open(filename) as img:
                # Check image format and convert if necessary
                if img.format != 'JPEG':
                    img.convert("RGB").save(destination_path, "JPEG")
                else:
                    img.save(destination_path, "JPEG")
        except Exception as e:
            messagebox.showwarning("Warning", f"Failed to process {filename}: {e}")

    messagebox.showinfo("Success", "Thumbnails have been registered successfully!")
