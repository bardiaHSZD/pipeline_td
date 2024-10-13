import os
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QSplitter, QPushButton
from PySide6.QtCore import Qt
from file_view import FileView
from asset_grid import AssetGrid
from preview_panel import PreviewPanel
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
        main_layout = QVBoxLayout()

        # Create splitter for adjustable sections (folder structure, grid view, and preview)
        self.splitter = QSplitter(Qt.Horizontal)

        # 1. Left Panel - Folder Structure (Tree View) with checkboxes and a Refresh Button
        left_layout = QVBoxLayout()
        self.file_view = FileView('assets/')
        left_layout.addWidget(self.file_view)

        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_assets)
        left_layout.addWidget(self.refresh_button)

        # Create left panel widget and add to splitter
        left_panel = QWidget()
        left_panel.setLayout(left_layout)
        self.splitter.addWidget(left_panel)

        # 2. Center Panel - Asset Grid View with Pagination
        center_layout = QVBoxLayout()

        # Asset Grid
        self.asset_grid = AssetGrid()
        center_layout.addWidget(self.asset_grid.asset_scroll)

        # Pagination
        self.pagination = Pagination(self.asset_grid, self)
        center_layout.addLayout(self.pagination.layout)

        # Create center panel widget and add to splitter
        center_panel = QWidget()
        center_panel.setLayout(center_layout)
        self.splitter.addWidget(center_panel)

        # 3. Right Panel - Asset Preview and Metadata
        self.preview_panel = PreviewPanel(self)
        right_panel = QWidget()
        right_panel.setLayout(self.preview_panel.create_preview_layout())

        # Add right panel to splitter
        self.splitter.addWidget(right_panel)

        # Set initial sizes of each panel in the splitter
        self.splitter.setSizes([300, 700, 300])

        # Add the splitter to the main layout
        main_layout.addWidget(self.splitter)

        # Set the main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Initially, show nothing in the grid (no folder selected)
        self.asset_files = []
        self.total_assets = 0
        self.pagination.update_grid()

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

    def load_assets(self, folder_paths):
        """Loads image assets from the given folders and their subfolders."""
        asset_files = []
        for folder_path in folder_paths:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        asset_files.append(os.path.join(root, file))
        return asset_files

    def show_asset_preview(self, asset_file):
        """Shows the selected asset in the preview section."""
        self.preview_panel.show_asset_preview(asset_file)
        self.selected_asset_file = asset_file  # Store the selected asset for sharing
