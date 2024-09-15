from tkinter import filedialog, messagebox

def open_folder_dialog(entry_field, root):
    folder = filedialog.askdirectory(title="Select Folder", parent=root)
    if folder:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, folder)

def exit_program(root):
    root.quit()

def show_about():
    messagebox.showinfo("About", "Copyright EEFA FX 2024")
