import os  # Import the os module
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt

class FileView(QTreeWidget):
    def __init__(self, folder_path):
        super().__init__()
        self.setHeaderHidden(True)  # Hide the header for a cleaner look
        self.load_folders(folder_path, self.invisibleRootItem())

    def load_folders(self, folder_path, parent_item):
        """Recursively load folders and subfolders into the QTreeWidget with checkboxes."""
        for entry in os.listdir(folder_path):
            full_path = os.path.join(folder_path, entry)
            if os.path.isdir(full_path):
                folder_item = QTreeWidgetItem(parent_item, [entry])
                folder_item.setData(0, Qt.UserRole, full_path)  # Store full path as data
                folder_item.setFlags(folder_item.flags() | Qt.ItemIsUserCheckable)  # Enable checkbox
                folder_item.setCheckState(0, Qt.Unchecked)  # Initialize checkbox as unchecked
                self.load_folders(full_path, folder_item)

    def get_selected_folders(self):
        """Returns a list of selected folders (those with checked checkboxes)."""
        selected_folders = []
        root = self.invisibleRootItem()
        for i in range(root.childCount()):
            folder_item = root.child(i)
            self._collect_selected_folders(folder_item, selected_folders)
        return selected_folders

    def _collect_selected_folders(self, item, selected_folders):
        """Recursively collect selected folders."""
        if item.checkState(0) == Qt.Checked:
            selected_folders.append(item.data(0, Qt.UserRole))  # Add folder path to the list
        for i in range(item.childCount()):
            self._collect_selected_folders(item.child(i), selected_folders)
