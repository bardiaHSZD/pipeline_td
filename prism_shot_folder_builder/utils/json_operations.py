import json
import os
from tkinter import messagebox

def generate_json_action(window, button, shots_folder_entry, save_path_entry):
    shots_folder = shots_folder_entry.get()
    save_path = save_path_entry.get()

    if not shots_folder or not save_path:
        messagebox.showerror("Error", "Please select both SHOTS folder and Save location.")
        return

    generate_shotinfo(shots_folder, save_path)
    window.destroy()

def generate_shotinfo(shots_folder, save_path):
    shot_ranges = {}
    start_frame = 1001

    for seq_folder in os.listdir(shots_folder):
        if seq_folder.startswith("seq_") and seq_folder[4:].isdigit():
            seq_path = os.path.join(shots_folder, seq_folder)
            if os.path.isdir(seq_path):
                shot_ranges[seq_folder] = {}
                for sh_folder in os.listdir(seq_path):
                    if sh_folder.startswith("SH") and sh_folder[2:].isdigit():
                        nk_path = os.path.join(seq_path, sh_folder, "Scenefiles", "COMPOSITE", "MAINCOMP")
                        end_frame = find_last_frame_in_nk_file(nk_path)
                        shot_ranges[seq_folder][sh_folder] = [start_frame, end_frame]

    shotinfo = {"shotRanges": shot_ranges}

    with open(os.path.join(save_path, 'shotinfo.json'), 'w') as json_file:
        json.dump(shotinfo, json_file, indent=4)
    messagebox.showinfo("Success", "Shots registered successfully!")

def find_last_frame_in_nk_file(folder_path):
    if not os.path.exists(folder_path):
        return 1100

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".nk"):
            nk_file_path = os.path.join(folder_path, file_name)
            with open(nk_file_path, 'r') as nk_file:
                for line in nk_file:
                    if 'last_frame' in line:
                        try:
                            return int(line.split()[1])
                        except (IndexError, ValueError):
                            messagebox.showerror("Error", f"Invalid last_frame format in {nk_file_path}")
                            return 1100
    return 1100
