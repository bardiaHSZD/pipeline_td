import os
import subprocess
import json
from PySide6.QtWidgets import QVBoxLayout, QLabel, QFormLayout, QPushButton, QHBoxLayout, QMessageBox, QDialog, QDialogButtonBox, QScrollArea, QWidget
from PySide6.QtGui import QPixmap, QGuiApplication
from PySide6.QtCore import Qt

def load_json_metadata(json_file_path):
    """Load metadata from the specified JSON file."""
    if not os.path.exists(json_file_path):
        return {"version": "N/A", "extension": "N/A", "department": "N/A", "task": "N/A", "global_path": None}  # Return default values if the file does not exist

    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    version = data.get("version", "N/A")  # Get the version
    global_path = data.get("locations", {}).get("global", None)  # Get the file's global path if it exists
    extension = os.path.splitext(global_path)[1] if global_path else "N/A"  # Get the file extension from global path
    department = data.get("department", "N/A")  # Get the department
    task = data.get("task", "N/A")  # Get the task

    return {"version": version, "extension": extension, "department": department, "task": task, "global_path": global_path}


class PreviewPanel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.scale_factor = 1.0  # Initial scale factor for zooming

        # Create scroll area for preview image
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Label to hold the preview image
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.scroll_area.setWidget(self.preview_label)

        # Metadata fields
        self.metadata_label = QLabel("No asset selected")
        self.version_label = QLabel("N/A")
        self.extension_label = QLabel("N/A")
        self.department_label = QLabel("N/A")  # Display department
        self.task_label = QLabel("N/A")  # Display task

    def create_preview_layout(self):
        """Creates the preview layout with scroll and zoom support."""
        preview_layout = QVBoxLayout()

        # Add the scroll area containing the preview label
        preview_layout.addWidget(self.scroll_area)

        # Metadata and Details Section
        metadata_layout = QFormLayout()
        metadata_layout.addRow("Asset Name:", self.metadata_label)
        metadata_layout.addRow("Version:", self.version_label)
        metadata_layout.addRow("Extension:", self.extension_label)
        metadata_layout.addRow("Department:", self.department_label)  # Display department
        metadata_layout.addRow("Task:", self.task_label)  # Display task

        preview_layout.addLayout(metadata_layout)

        # Buttons for "Share" and "Open in Explorer"
        button_layout = QHBoxLayout()
        self.share_button = QPushButton("Share")
        self.share_button.clicked.connect(self.share_asset)
        self.open_explorer_button = QPushButton("Open in Explorer")
        self.open_explorer_button.clicked.connect(self.open_in_explorer)
        button_layout.addWidget(self.share_button)
        button_layout.addWidget(self.open_explorer_button)

        preview_layout.addLayout(button_layout)

        return preview_layout

    def show_asset_preview(self, asset_file):
        """Displays the selected asset image in the preview section."""
        asset_path = os.path.abspath(asset_file)

        pixmap = QPixmap(asset_path)
        if pixmap.isNull():
            self.preview_label.setText("Error loading preview")
        else:
            self.scale_factor = 1.0  # Reset zoom when a new image is loaded
            self.preview_label.setPixmap(pixmap.scaled(400, 200, Qt.KeepAspectRatio))  # Reduced height to 200

        # Load metadata from the corresponding JSON file
        json_file_path = f"{os.path.splitext(asset_file)[0]}versioninfo.json"  # Construct the JSON file path
        metadata = load_json_metadata(json_file_path)  # Load version, extension, department, task, and global_path

        # Set metadata
        asset_name = os.path.basename(asset_file)
        asset_name_without_extension = os.path.splitext(asset_name)[0]  # Remove the file extension
        self.metadata_label.setText(asset_name_without_extension)
        self.version_label.setText(f"{metadata['version']}")
        self.extension_label.setText(f"{metadata['extension']}")
        self.department_label.setText(f"{metadata['department']}")  # Set department
        self.task_label.setText(f"{metadata['task']}")  # Set task

    def share_asset(self):
        """Displays a window with the asset path and a copy to clipboard button."""
        if not self.parent.selected_asset_file:
            QMessageBox.warning(self.parent, "No Asset Selected", "Please select an asset to share.")
            return

        full_path = os.path.abspath(self.parent.selected_asset_file)
        json_file_path = f"{os.path.splitext(full_path)[0]}versioninfo.json"  # Corresponding JSON file path
        metadata = load_json_metadata(json_file_path)

        # If JSON exists and global path is available, use the global path, otherwise use the asset's folder
        if metadata and metadata["global_path"]:
            share_path = metadata["global_path"]
        else:
            # If no global path, use the folder path of the thumbnail
            share_path = os.path.dirname(full_path)

        # Create a dialog window to show the path and allow copying
        dialog = QDialog(self.parent)
        dialog.setWindowTitle("Share Asset Path")
        dialog_layout = QVBoxLayout()

        # Show the full path of the asset or global path
        path_label = QLabel(f"Full path:\n{share_path}")
        dialog_layout.addWidget(path_label)

        # Create the "Copy to Clipboard" and "OK" buttons
        button_box = QDialogButtonBox()

        # Copy to Clipboard button
        copy_button = QPushButton("Copy to Clipboard")
        copy_button.clicked.connect(lambda: self.copy_to_clipboard(share_path))
        button_box.addButton(copy_button, QDialogButtonBox.ActionRole)

        # OK button to close the dialog
        ok_button = button_box.addButton(QDialogButtonBox.Ok)
        ok_button.clicked.connect(dialog.accept)

        dialog_layout.addWidget(button_box)
        dialog.setLayout(dialog_layout)
        dialog.exec()

    def copy_to_clipboard(self, text):
        """Copies the provided text to the system clipboard."""
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(text)
        QMessageBox.information(self.parent, "Copied", "Asset path copied to clipboard!")

    def open_in_explorer(self):
        """Opens the selected asset in the file explorer and selects the file."""
        if not self.parent.selected_asset_file:
            QMessageBox.warning(self.parent, "No Asset Selected", "Please select an asset to open in explorer.")
            return

        full_path = os.path.abspath(self.parent.selected_asset_file)

        try:
            subprocess.run(['explorer', '/select,', full_path])
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Could not open file in explorer: {str(e)}")
