import os
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QFormLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox, QDialog, QVBoxLayout, QDialogButtonBox
from PySide6.QtGui import QPixmap, QGuiApplication
from PySide6.QtCore import Qt
from file_view import FileView
from asset_grid import AssetGrid
from pagination import Pagination

class AssetBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Asset Browser")
        self.setGeometry(100, 100, 1300, 800)

        # Initialize attributes for pagination
        self.current_page = 0
        self.total_assets = 0
        self.selected_folders = []  # Track all selected folders
        self.selected_asset_file = None  # Track the selected asset file for sharing

        # Main layout setup
        main_layout = QHBoxLayout()

        # 1. Left Panel - Folder Structure (Tree View) with checkboxes and a Refresh Button
        left_layout = QVBoxLayout()
        self.file_view = FileView('assets/')
        left_layout.addWidget(self.file_view)
        
        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_assets)
        left_layout.addWidget(self.refresh_button)

        main_layout.addLayout(left_layout, 1)

        # 2. Center Panel - Asset Grid View with Pagination
        center_layout = QVBoxLayout()

        # Search and filter options
        search_layout = self.create_search_layout()
        center_layout.addLayout(search_layout)

        # Asset Grid
        self.asset_grid = AssetGrid()
        center_layout.addWidget(self.asset_grid.asset_scroll)

        # Pagination
        self.pagination = Pagination(self.asset_grid, self)
        center_layout.addLayout(self.pagination.layout)

        main_layout.addLayout(center_layout, 3)

        # Right Panel - Asset Preview and Metadata
        preview_layout = self.create_preview_layout()
        main_layout.addLayout(preview_layout, 1)

        # Set the main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Initially, show nothing in the grid (no folder selected)
        self.asset_files = []
        self.total_assets = 0
        self.pagination.update_grid()

    def load_assets(self, folder_paths):
        """Loads image assets from the given folders and their subfolders."""
        asset_files = []
        for folder_path in folder_paths:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        asset_files.append(os.path.join(root, file))
        return asset_files

    def refresh_assets(self):
        """Handles refreshing of asset grid based on selected folders."""
        # Clear the currently selected folders
        self.selected_folders = self.file_view.get_selected_folders()  # Get selected folders

        if not self.selected_folders:
            # No folder selected, clear the grid
            self.asset_files = []
            self.total_assets = 0
            self.pagination.update_grid()
        else:
            # Load assets from all selected folders
            self.asset_files = self.load_assets(self.selected_folders)
            self.total_assets = len(self.asset_files)
            self.current_page = 0  # Reset pagination to the first page
            self.pagination.update_grid()

    def create_search_layout(self):
        """Creates the search and filter layout."""
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search")
        self.exclude_input = QLineEdit()
        self.exclude_input.setPlaceholderText("Exclude")

        self.production_dropdown = QComboBox()
        self.production_dropdown.addItems(["Production", "All", "Specific Production"])

        self.client_dropdown = QComboBox()
        self.client_dropdown.addItems(["Client", "All", "Client 1", "Client 2"])

        self.type_dropdown = QComboBox()
        self.type_dropdown.addItems(["Type", "All", "Image", "3D Model"])

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.exclude_input)
        search_layout.addWidget(self.production_dropdown)
        search_layout.addWidget(self.client_dropdown)
        search_layout.addWidget(self.type_dropdown)

        return search_layout

    def create_preview_layout(self):
        """Creates the asset preview and metadata layout."""
        preview_layout = QVBoxLayout()

        # Preview Image
        self.preview_label = QLabel("Preview")
        self.preview_label.setAlignment(Qt.AlignCenter)  # Align center
        self.preview_label.setFixedSize(300, 300)  # Placeholder for preview image
        self.preview_label.setStyleSheet("border: 1px solid #ccc;")
        preview_layout.addWidget(self.preview_label)

        # Metadata and Details Section
        metadata_layout = QFormLayout()
        self.metadata_label = QLabel("No asset selected")
        self.version_label = QLabel("Version: N/A")
        self.production_label = QLabel("Production: N/A")
        self.client_label = QLabel("Client: N/A")
        metadata_layout.addRow("Asset Name:", self.metadata_label)
        metadata_layout.addRow("Version:", self.version_label)
        metadata_layout.addRow("Production:", self.production_label)
        metadata_layout.addRow("Client:", self.client_label)

        preview_layout.addLayout(metadata_layout)

        # Tags Section
        self.tags_label = QLabel("Tags:")
        self.tags_input = QLineEdit()
        preview_layout.addWidget(self.tags_label)
        preview_layout.addWidget(self.tags_input)

        # Buttons for "Share" and "Open in Explorer"
        button_layout = QHBoxLayout()
        self.share_button = QPushButton("Share")
        self.share_button.clicked.connect(self.share_asset)  # Connect to share action
        self.open_explorer_button = QPushButton("Open in Explorer")
        button_layout.addWidget(self.share_button)
        button_layout.addWidget(self.open_explorer_button)

        preview_layout.addLayout(button_layout)

        return preview_layout

    def show_asset_preview(self, asset_file):
        """Shows the selected asset in the preview section."""
        asset_path = os.path.join(asset_file)  # Get the full path to the asset
        self.selected_asset_file = asset_path  # Store the selected asset for sharing

        # Check if the image exists before attempting to display it
        if not os.path.exists(asset_path):
            self.preview_label.setText("No preview available")
            return

        # Load the image into a QPixmap and scale it for the preview
        pixmap = QPixmap(asset_path)
        if pixmap.isNull():
            self.preview_label.setText("Error loading preview")
        else:
            pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
            self.preview_label.setPixmap(pixmap)

        # Set metadata (In a real app, you'd load this from a database or file)
        self.metadata_label.setText(asset_file)
        self.version_label.setText("Version: 1")
        self.production_label.setText("Production: Bunderkin")
        self.client_label.setText("Client: None")

    def share_asset(self):
        """Displays a window with the asset path and a copy to clipboard button."""
        if not self.selected_asset_file:
            QMessageBox.warning(self, "No Asset Selected", "Please select an asset to share.")
            return

        # Convert the relative path to an absolute path and normalize it for Windows
        full_path = os.path.abspath(self.selected_asset_file)
        full_path = os.path.normpath(full_path)  # Normalize the path to use backslashes for Windows

        # Create a dialog window to show the path and allow copying
        dialog = QDialog(self)
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
        button_box.addButton(copy_button, QDialogButtonBox.ActionRole)  # Add copy button to the left

        # OK button to close the dialog
        ok_button = button_box.addButton(QDialogButtonBox.Ok)
        ok_button.clicked.connect(dialog.accept)  # Close the dialog when OK is pressed

        # Add buttons to the layout
        dialog_layout.addWidget(button_box)

        dialog.setLayout(dialog_layout)
        dialog.exec()

    def copy_to_clipboard(self, text):
        """Copies the provided text to the system clipboard."""
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(text)
        QMessageBox.information(self, "Copied", "Asset path copied to clipboard!")
