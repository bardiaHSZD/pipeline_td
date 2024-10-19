import os
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QProgressBar, QPushButton, QLineEdit, QComboBox, QCompleter
from PySide6.QtCore import QTimer, QStringListModel, Qt
from file_view import FileView
from asset_grid import AssetGrid
from pagination import Pagination
from preview_panel import PreviewPanel
from trie import Trie
from asset_helper import AssetHelper  # Import the helper module
import re

class AssetBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Asset Browser")
        self.setGeometry(100, 100, 1300, 800)

        self.current_page = 0
        self.items_per_page = 12  # Set 12 items per page (4 rows x 3 columns)
        self.trie = Trie()  # Initialize the Trie for prefix search

        self.asset_helper = AssetHelper()  # Initialize the helper class
        self.all_asset_files = []  # Keep all loaded assets here
        self.filtered_asset_files = []  # Keep filtered assets here
        self.total_assets = 0  # Initialize total_assets

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

        # Initialize Pagination after total_assets is set
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

        self.filtered_asset_files = []
        self.total_assets = 0
        self.pagination.update_grid()

        # Create a completer for the search input field
        self.completer_model = QStringListModel()  # To store the autocomplete suggestions
        self.completer = QCompleter(self.completer_model)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)  # Make it case insensitive
        self.search_input.setCompleter(self.completer)

    def create_search_layout(self):
        """Creates the search and filter layout with search and tags input."""
        search_layout = QHBoxLayout()

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search")
        self.search_input.textChanged.connect(self.update_completer)  # Update completer on typing
        search_layout.addWidget(self.search_input)

        # Tags input (replacing the Exclude input)
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Tags")
        search_layout.addWidget(self.tags_input)

        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.filter_assets)  # Trigger search on button click
        search_layout.addWidget(self.search_button)

        # Client dropdown
        self.client_dropdown = QComboBox()
        self.client_dropdown.addItems(["Client", "All", "Client 1", "Client 2"])
        search_layout.addWidget(self.client_dropdown)

        # Asset type dropdown
        self.type_dropdown = QComboBox()
        self.type_dropdown.addItems(["Type", "All", "Image", "3D Model"])
        search_layout.addWidget(self.type_dropdown)

        return search_layout

    def refresh_assets(self):
        """Handles refreshing of asset grid based on selected folders."""
        self.selected_folders = self.file_view.get_selected_folders()  # Get selected folders

        # Clear the search input when refreshing
        self.search_input.clear()  # Clear the search text field

        if not self.selected_folders:
            # No folder selected, clear the grid
            self.all_asset_files = []
            self.filtered_asset_files = []
            self.total_assets = 0
            self.pagination.update_grid()
        else:
            # Load assets using the helper
            self.all_asset_files = self.asset_helper.load_assets(self.selected_folders)
            self.filtered_asset_files = self.all_asset_files  # Initially, show all assets
            self.total_assets = len(self.all_asset_files)
            self.current_page = 0  # Reset pagination to the first page

            # Insert asset file names into the Trie for prefix search
            self.trie = Trie()  # Clear the trie
            for asset_file in self.all_asset_files:
                asset_name = os.path.basename(asset_file)
                self.trie.insert(asset_name)

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
        chunk_end = min(start_index + self.loaded_assets + 12, end_index)

        # Load the assets for this chunk into the grid
        self.asset_grid.load_assets(self.filtered_asset_files, start_index + self.loaded_assets, chunk_end, self)

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

    def update_completer(self):
        """Update the QCompleter with suggestions based on the search text."""
        search_text = self.search_input.text().lower()

        if search_text == "":
            self.completer_model.setStringList([])  # Clear suggestions if no input
            return

        # Get suggestions from the Trie
        suggestions = self.trie.search(search_text)

        # Set the top 12 suggestions for the completer, without file extensions
        suggestions = [os.path.splitext(suggestion)[0] for suggestion in suggestions]
        self.completer_model.setStringList(suggestions[:12])


    def filter_assets(self):
        """Filter assets in the grid based on the search input and tags when the Search button is clicked."""
        search_text = self.search_input.text().lower()
        tag_text = self.tags_input.text().lower()

        # Parse the tag text for AND/OR operations with brackets
        tag_expression = self.parse_tag_text(tag_text)

        # Use the helper method to find matching assets based on search and parsed tag expression
        matching_assets = self.asset_helper.filter_assets(search_text, tag_expression, self.all_asset_files)

        self.filtered_asset_files = matching_assets

        # Update the total number of assets and reset pagination
        self.total_assets = len(self.filtered_asset_files)
        self.current_page = 0
        self.pagination.update_grid()

    def parse_tag_text(self, tag_text):
        """Parse the tag text input and return a structure that supports complex AND/OR logic with brackets."""
        if not tag_text:
            return []

        # Tokenize input with spaces, AND, OR, and brackets
        tokens = re.findall(r'\(|\)|\band\b|\bor\b|#[\w_-]+', tag_text, re.IGNORECASE)

        def parse_expression(index=0):
            """Recursively parse the token list into a structured logical expression."""
            result = []
            current_group = []
            current_op = None  # Keeps track of the current logical operation (AND/OR)

            while index < len(tokens):
                token = tokens[index].lower()

                if token == '(':
                    # Start a new group and recursively parse it
                    sub_expression, index = parse_expression(index + 1)
                    current_group.append(sub_expression)
                elif token == ')':
                    # End of a group, return it
                    if current_group:
                        result.append(('AND', current_group) if current_op == 'and' else ('OR', current_group))
                    return result, index
                elif token in ('and', 'or'):
                    # Logical operator (AND/OR)
                    if current_group:
                        result.append(('AND', current_group) if current_op == 'and' else ('OR', current_group))
                    current_op = token
                    current_group = []
                else:
                    # It's a tag (e.g., #3D_asset)
                    current_group.append(token)

                index += 1

            # Add the final group
            if current_group:
                result.append(('AND', current_group) if current_op == 'and' else ('OR', current_group))
            return result, index

        expression, _ = parse_expression()
        return expression
