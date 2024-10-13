import os
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

class FileView(QTreeWidget):
    def __init__(self, folder_path):
        super().__init__()
        self.setHeaderHidden(False)
        self.setHeaderLabel("Folder Structure")
        self.load_folders(folder_path, self.invisibleRootItem())

    def load_folders(self, folder_path, parent_item):
        """Recursively load folders and subfolders into the QTreeWidget."""
        for entry in os.listdir(folder_path):
            full_path = os.path.join(folder_path, entry)
            if os.path.isdir(full_path):
                folder_item = QTreeWidgetItem(parent_item, [entry])
                self.load_folders(full_path, folder_item)
