import os  # Import os module for file and directory operations
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QFormLayout, QLabel, QLineEdit, QComboBox, QPushButton
from PySide6.QtGui import QPixmap  # Import QPixmap for handling images
from PySide6.QtCore import Qt  # Import Qt for alignment
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

        # Main layout setup
        main_layout = QHBoxLayout()

        # 1. Left Panel - Folder Structure (Tree View)
        self.file_view = FileView('assets/')
        main_layout.addWidget(self.file_view, 1)  # 1/4th of the width

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

        main_layout.addLayout(center_layout, 3)  # 3/4th width for asset grid and pagination

        # Right Panel - Asset Preview and Metadata
        preview_layout = self.create_preview_layout()
        main_layout.addLayout(preview_layout, 1)

        # Set the main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Load assets from the folder
        self.asset_files = self.load_assets()
        self.total_assets = len(self.asset_files)  # Update total assets count
        self.pagination.update_grid()  # Load the first page of assets

    def load_assets(self):
        """Loads image assets from the 'assets/' folder."""
        assets_folder = 'assets/'  # Specify the folder where your images are stored
        asset_files = [f for f in os.listdir(assets_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        return asset_files

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

        # Buttons for "Open" and "Open in Explorer"
        button_layout = QHBoxLayout()
        self.open_button = QPushButton("Open")
        self.open_explorer_button = QPushButton("Open in Explorer")
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.open_explorer_button)

        preview_layout.addLayout(button_layout)

        return preview_layout

    def show_asset_preview(self, asset_file):
        """Shows the selected asset in the preview section."""
        asset_path = os.path.join('assets/', asset_file)

        # Set the preview image
        pixmap = QPixmap(asset_path).scaled(300, 300, Qt.KeepAspectRatio)
        self.preview_label.setPixmap(pixmap)

        # Set metadata (In a real app, you'd load this from a database or file)
        self.metadata_label.setText(asset_file)
        self.version_label.setText("Version: 1")
        self.production_label.setText("Production: Bunderkin")
        self.client_label.setText("Client: None")
