import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt


class FileView(QWidget):
    def __init__(self, root_folder):
        super().__init__()
        self.root_folder = root_folder
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Folders")

        # Load initial folder structure without displaying the root folder itself
        self.load_folders(root_folder)

        # Connect the itemChanged signal to handle checkbox state changes
        self.tree.itemChanged.connect(self.item_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        self.setLayout(layout)

    def load_folders(self, folder_path, parent_item=None):
        """Recursively load folders and create tree items with checkboxes."""
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                folder_item = QTreeWidgetItem(parent_item or self.tree, [item])
                folder_item.setFlags(folder_item.flags() | Qt.ItemIsUserCheckable)  # Set item to be user checkable
                folder_item.setCheckState(0, Qt.Unchecked)  # Set initial checkbox state
                self.load_folders(item_path, folder_item)  # Recursive call for subfolders

    def get_selected_folders(self):
        """Return a list of unique selected folders based on checkbox states."""
        selected_folders = set()  # Use a set to avoid duplicates
        self._get_selected_folders_recursive(self.tree.invisibleRootItem(), selected_folders)
        return list(selected_folders)  # Convert back to list for returning

    def _get_selected_folders_recursive(self, tree_item, selected_folders):
        """Recursive function to gather selected folders."""
        for index in range(tree_item.childCount()):
            child_item = tree_item.child(index)
            if child_item.checkState(0) == Qt.Checked:
                # If checked, add the full path of the folder to the set
                full_path = self._get_full_path(child_item)
                selected_folders.add(full_path)  # Add to the set for uniqueness
            # Check if the parent is checked to avoid adding its children separately
            elif child_item.checkState(0) == Qt.Unchecked:
                self._get_selected_folders_recursive(child_item, selected_folders)

    def _get_full_path(self, item):
        """Return the full path for the given tree item."""
        parts = []
        while item:
            parts.append(item.text(0))
            item = item.parent()
        return os.path.join(self.root_folder, *reversed(parts))  # Return the full path

    def item_changed(self, item, column):
        """Handle checkbox state change."""
        if item.checkState(column) == Qt.Checked:
            self.set_item_checked(item, Qt.Checked)  # Check all children
        else:
            self.set_item_checked(item, Qt.Unchecked)  # Uncheck all children

    def set_item_checked(self, item, state):
        """Set the checkbox state for an item and all its children."""
        item.setCheckState(0, state)
        for index in range(item.childCount()):
            self.set_item_checked(item.child(index), state)

# Ensure to test this class properly to confirm that it behaves as expected
