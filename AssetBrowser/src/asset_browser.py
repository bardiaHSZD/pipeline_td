import os
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QProgressBar, QPushButton, QLineEdit, QComboBox
from PySide6.QtCore import QTimer
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
        self.items_per_page = 12  # Set 12 items per page (4 rows x 3 columns)

        # Main layout setup
        main_layout = QVBoxLayout()

        # Search and filter options layout
        search_layout = self.create_search_layout()
        main_layout.addLayout(search_layout)

        # Top Layout (Grid, Pagination, and Folder Structure)
        top_layout = QHBoxLayout()

        # Left Panel - Folder Structure
        left_layout = QVBoxLayout()
        self.file_view = FileView('assets/')
        left_layout.addWidget(self.file_view)

        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_assets)  # Trigger progress on refresh
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

    def create_search_layout(self):
        """Creates the search and filter layout with search, exclude, and dropdowns."""
        search_layout = QHBoxLayout()

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search")
        search_layout.addWidget(self.search_input)

        # Exclude input
        self.exclude_input = QLineEdit()
        self.exclude_input.setPlaceholderText("Exclude")
        search_layout.addWidget(self.exclude_input)

        # Production dropdown
        self.production_dropdown = QComboBox()
        self.production_dropdown.addItems(["Production", "All", "Specific Production"])
        search_layout.addWidget(self.production_dropdown)

        # Client dropdown
        self.client_dropdown = QComboBox()
        self.client_dropdown.addItems(["Client", "All", "Client 1", "Client 2"])
        search_layout.addWidget(self.client_dropdown)

        # Asset type dropdown
        self.type_dropdown = QComboBox()
        self.type_dropdown.addItems(["Type", "All", "Image", "3D Model"])
        search_layout.addWidget(self.type_dropdown)

        return search_layout

    def load_assets(self, folder_paths):
        """Load image assets from the selected folders and their subfolders."""
        asset_files = []
        for folder_path in folder_paths:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        asset_files.append(os.path.join(root, file))

        # Filter the assets based on search and exclude input
        search_term = self.search_input.text().lower()
        exclude_term = self.exclude_input.text().lower()

        if search_term:
            asset_files = [f for f in asset_files if search_term in os.path.basename(f).lower()]
        if exclude_term:
            asset_files = [f for f in asset_files if exclude_term not in os.path.basename(f).lower()]

        return asset_files

    def refresh_assets(self):
        """Handles refreshing of asset grid based on selected folders."""
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

    def load_assets_in_chunks(self, start_index, end_index):
        """Load assets for the current page in smaller chunks and update the progress bar."""
        self.loaded_assets = 0  # Track how many assets have been loaded
        self.total_to_load = end_index - start_index  # Total assets to load on the current page

        # Set progress bar maximum based on the number of assets to load on this page
        self.progress_bar.setMaximum(self.total_to_load)
        self.progress_bar.setValue(0)  # Reset the progress bar to 0

        # Start the chunked loading process
        self.asset_chunk_timer = QTimer(self)
        self.asset_chunk_timer.timeout.connect(lambda: self.load_next_chunk(start_index, end_index))
        self.asset_chunk_timer.start(100)  # Load assets in chunks every 100 ms

    def load_next_chunk(self, start_index, end_index):
        """Load the next chunk of assets for the current page and update the progress bar."""
        chunk_end = min(start_index + self.loaded_assets + 4, end_index)

        # Load the assets for this chunk into the grid
        self.asset_grid.load_assets(self.asset_files, start_index + self.loaded_assets, chunk_end, self)

        # Update the progress bar
        self.loaded_assets = chunk_end - start_index  # Update the number of loaded assets for this page
        self.progress_bar.setValue(self.loaded_assets)

        # Stop the timer when all assets for the page are loaded
        if self.loaded_assets >= (end_index - start_index):
            self.asset_chunk_timer.stop()

    def show_asset_preview(self, asset_file):
        """Shows the selected asset in the preview section."""
        self.preview_panel.show_asset_preview(asset_file)
        self.selected_asset_file = asset_file  # Store the selected asset for sharing or opening
