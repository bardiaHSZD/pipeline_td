import os
import subprocess
from PySide6.QtWidgets import QVBoxLayout, QLabel, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QDialog, QDialogButtonBox
from PySide6.QtGui import QPixmap, QGuiApplication
from PySide6.QtCore import Qt


class PreviewPanel:
    def __init__(self, parent):
        self.parent = parent
        self.preview_label = QLabel("Preview")
        self.metadata_label = QLabel("No asset selected")
        self.version_label = QLabel("Version: N/A")
        self.production_label = QLabel("Production: N/A")
        self.client_label = QLabel("Client: N/A")
        self.tags_input = QLineEdit()

    def create_preview_layout(self):
        preview_layout = QVBoxLayout()

        # Preview Image
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setFixedSize(400, 400)  # Increase the size of the preview image
        self.preview_label.setStyleSheet("")  # Remove the white border
        preview_layout.addWidget(self.preview_label)

        # Metadata and Details Section
        metadata_layout = QFormLayout()
        metadata_layout.addRow("Asset Name:", self.metadata_label)
        metadata_layout.addRow("Version:", self.version_label)
        metadata_layout.addRow("Production:", self.production_label)
        metadata_layout.addRow("Client:", self.client_label)

        preview_layout.addLayout(metadata_layout)

        # Tags Section
        preview_layout.addWidget(QLabel("Tags:"))
        preview_layout.addWidget(self.tags_input)

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
        """Shows the selected asset in the preview section."""
        # Convert the relative path to an absolute path
        asset_path = os.path.abspath(asset_file)

        # Load the image into a QPixmap and scale it for the preview
        pixmap = QPixmap(asset_path)
        if pixmap.isNull():
            self.preview_label.setText("Error loading preview")
        else:
            pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)  # Larger size
            self.preview_label.setPixmap(pixmap)

        # Set metadata (In a real app, you'd load this from a database or file)
        self.metadata_label.setText(os.path.basename(asset_file))
        self.version_label.setText("Version: 1")
        self.production_label.setText("Production: Bunderkin")
        self.client_label.setText("Client: None")

    def share_asset(self):
        """Displays a window with the asset path and a copy to clipboard button."""
        if not self.parent.selected_asset_file:
            QMessageBox.warning(self.parent, "No Asset Selected", "Please select an asset to share.")
            return

        full_path = os.path.abspath(self.parent.selected_asset_file)

        # Create a dialog window to show the path and allow copying
        dialog = QDialog(self.parent)
        dialog.setWindowTitle("Share Asset Path")
        dialog_layout = QVBoxLayout()

        # Show the full path of the selected asset
        path_label = QLabel(f"Full path:\n{full_path}")
        dialog_layout.addWidget(path_label)

        # Create the "Copy to Clipboard" and "OK" buttons
        button_box = QDialogButtonBox()

        # Copy to Clipboard button
        copy_button = QPushButton("Copy to Clipboard")
        copy_button.clicked.connect(lambda: self.copy_to_clipboard(full_path))
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
