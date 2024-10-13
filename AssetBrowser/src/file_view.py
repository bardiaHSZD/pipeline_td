import os
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
from PySide6.QtCore import Qt  # Import Qt for setting checkbox state


class FileView(QWidget):
    def __init__(self, root_folder):
        super().__init__()
        self.root_folder = root_folder

        # Create the tree view for displaying folders with checkboxes
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)  # Hide headers for a cleaner look

        # Load the folder structure into the tree view with checkboxes
        self.load_folders(self.root_folder)

        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        self.setLayout(layout)

    def load_folders(self, folder_path):
        """Recursively load folders into the tree view with checkboxes."""
        for entry in os.listdir(folder_path):
            full_path = os.path.join(folder_path, entry)
            if os.path.isdir(full_path):
                folder_item = QTreeWidgetItem([entry])
                folder_item.setCheckState(0, Qt.Unchecked)  # Add checkbox for folder selection
                self.tree.addTopLevelItem(folder_item)
                self.add_subfolders(folder_item, full_path)

    def add_subfolders(self, parent_item, folder_path):
        """Add subfolders to the parent item recursively with checkboxes."""
        for entry in os.listdir(folder_path):
            full_path = os.path.join(folder_path, entry)
            if os.path.isdir(full_path):
                subfolder_item = QTreeWidgetItem([entry])
                subfolder_item.setCheckState(0, Qt.Unchecked)  # Add checkbox for subfolder
                parent_item.addChild(subfolder_item)
                self.add_subfolders(subfolder_item, full_path)

    def get_selected_folders(self):
        """Get all selected folders (with checked checkboxes)."""
        selected_folders = []

        def get_checked_folders(item):
            """Recursively gather folders that are checked."""
            if item.checkState(0) == Qt.Checked:
                folder_path = os.path.join(self.root_folder, item.text(0))
                selected_folders.append(folder_path)

            # Check subfolders
            for i in range(item.childCount()):
                get_checked_folders(item.child(i))

        # Iterate through all top-level items (root folders)
        for i in range(self.tree.topLevelItemCount()):
            get_checked_folders(self.tree.topLevelItem(i))

        return selected_folders
