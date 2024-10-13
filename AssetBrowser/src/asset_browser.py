import os
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QProgressBar
from file_view import FileView
from asset_grid import AssetGrid
from pagination import Pagination
from preview_panel import PreviewPanel


class AssetBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Asset Browser")
        self.setGeometry(100, 100, 1300, 800)

        self.current_page = 0
        self.total_assets = 0
        self.selected_folders = []
        self.selected_asset_file = None

        # Main layout setup
        main_layout = QVBoxLayout()

        # Top Layout (Grid, Pagination, and Folder Structure)
        top_layout = QHBoxLayout()

        # Left Panel - Folder Structure
        left_layout = QVBoxLayout()
        self.file_view = FileView('assets/')
        left_layout.addWidget(self.file_view)

        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_assets)
        left_layout.addWidget(self.refresh_button)

        top_layout.addLayout(left_layout, 1)

        # Center Panel - Asset Grid and Pagination
        center_layout = QVBoxLayout()
        self.asset_grid = AssetGrid(self)  # Pass in parent for progress bar
        center_layout.addWidget(self.asset_grid.asset_scroll)

        self.pagination = Pagination(self.asset_grid, self)
        center_layout.addLayout(self.pagination.layout)

        top_layout.addLayout(center_layout, 3)

        # Right Panel - Asset Preview
        self.preview_panel = PreviewPanel(self)
        top_layout.addLayout(self.preview_panel.create_preview_layout(), 1)

        main_layout.addLayout(top_layout)

        # Progress Bar at the bottom of the window (always visible, fixed height)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFixedHeight(20)  # Fixed height so the UI doesn't shift
        main_layout.addWidget(self.progress_bar)

        # Set the main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.asset_files = []
        self.total_assets = 0
        self.pagination.update_grid()

    def load_assets(self, folder_paths):
        asset_files = []
        for folder_path in folder_paths:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        asset_files.append(os.path.join(root, file))
        return asset_files

    def refresh_assets(self):
        self.selected_folders = self.file_view.get_selected_folders()
        if not self.selected_folders:
            self.asset_files = []
            self.total_assets = 0
        else:
            self.asset_files = self.load_assets(self.selected_folders)
            self.total_assets = len(self.asset_files)
            self.current_page = 0
        self.pagination.update_grid()

    def show_asset_preview(self, asset_file):
        self.preview_panel.show_asset_preview(asset_file)
        self.selected_asset_file = asset_file
