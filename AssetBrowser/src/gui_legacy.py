import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QWidget, QTreeWidget, QTreeWidgetItem, QGridLayout, QGroupBox, QPushButton, QScrollArea, QComboBox, QFormLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize, QEvent

ASSETS_PER_PAGE = 12  # Show 12 assets per page, but display only 6 at a time (scrollable)

class AssetBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Asset Browser")
        self.setGeometry(100, 100, 1300, 800)  # Adjusted window size

        # Main layout setup
        main_layout = QHBoxLayout()

        # 1. Left Panel - File View (Tree)
        self.file_view = QTreeWidget()
        self.file_view.setHeaderHidden(True)

        # Load and display the folder structure under the assets folder
        self.load_folders('assets/', self.file_view.invisibleRootItem())

        main_layout.addWidget(self.file_view, 1)  # File View gets 1/4th of the width

        # 2. Center Panel - Search and Asset Grid View
        center_layout = QVBoxLayout()
        search_layout = QHBoxLayout()

        # Search and Exclude Input Fields
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search")
        self.exclude_input = QLineEdit()
        self.exclude_input.setPlaceholderText("Exclude")

        # Filters: Production and Client dropdowns
        self.production_dropdown = QComboBox()
        self.production_dropdown.addItems(["Production", "All", "Specific Production"])
        self.client_dropdown = QComboBox()
        self.client_dropdown.addItems(["Client", "All", "Client 1", "Client 2"])
        self.type_dropdown = QComboBox()
        self.type_dropdown.addItems(["Type", "All", "Image", "3D Model"])

        # Add search, exclude, and dropdowns to layout
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.exclude_input)
        search_layout.addWidget(self.production_dropdown)
        search_layout.addWidget(self.client_dropdown)
        search_layout.addWidget(self.type_dropdown)

        center_layout.addLayout(search_layout)

        # Asset Grid Area (scrollable)
        self.asset_grid_group = QGroupBox("Assets")
        self.asset_grid_layout = QGridLayout()
        self.asset_grid_group.setLayout(self.asset_grid_layout)

        # Scroll area for assets (initially showing only 3x2 grid)
        self.asset_scroll = QScrollArea()
        self.asset_scroll.setWidgetResizable(True)
        self.asset_scroll.setWidget(self.asset_grid_group)

        center_layout.addWidget(self.asset_scroll)
        main_layout.addLayout(center_layout, 3)  # Asset Grid gets more space (2/3)

        # Pagination controls (next and previous buttons, page display)
        self.current_page = 0
        self.total_assets = 0

        pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.prev_page)

        self.page_number_input = QLineEdit()
        self.page_number_input.setFixedWidth(40)  # Set width for page number input
        self.page_number_input.setAlignment(Qt.AlignCenter)
        self.page_number_input.setText(str(self.current_page + 1))
        self.page_number_input.returnPressed.connect(self.jump_to_page)

        self.total_pages_label = QLabel("/ 1")  # Default label for total number of pages

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)

        # Add widgets to the pagination layout
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(QLabel("Page:"))
        pagination_layout.addWidget(self.page_number_input)
        pagination_layout.addWidget(self.total_pages_label)
        pagination_layout.addWidget(self.next_button)

        center_layout.addLayout(pagination_layout)

        # Load assets from the folder
        self.asset_files = self.load_assets()
        self.update_total_pages()
        self.display_assets()

        # 3. Right Panel - Asset Preview and Metadata
        preview_layout = QVBoxLayout()

        # Preview Image
        self.preview_label = QLabel("Preview")
        self.preview_label.setAlignment(Qt.AlignCenter)
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

        # Add right panel to main layout
        main_layout.addLayout(preview_layout, 1)  # Preview gets 1/4th width

        # Set main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Event filter for resizing the asset grid based on window size
        self.installEventFilter(self)

    def load_folders(self, folder_path, parent_item):
        """Recursively load folders and subfolders into the QTreeWidget."""
        for entry in os.listdir(folder_path):
            full_path = os.path.join(folder_path, entry)
            if os.path.isdir(full_path):
                folder_item = QTreeWidgetItem(parent_item, [entry])
                self.load_folders(full_path, folder_item)

    def load_assets(self):
        """Loads image assets from the 'assets/' folder."""
        assets_folder = 'assets/'  # Specify the folder where your images are stored
        asset_files = [f for f in os.listdir(assets_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        self.total_assets = len(asset_files)
        return asset_files

    def display_assets(self):
        """Displays assets for the current page (12 assets per page, with scrolling)."""
        start_index = self.current_page * ASSETS_PER_PAGE
        end_index = min(start_index + ASSETS_PER_PAGE, self.total_assets)

        # Clear the grid layout before loading new assets
        for i in reversed(range(self.asset_grid_layout.count())):
            widget = self.asset_grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Load and display each asset on the current page
        for idx, asset_file in enumerate(self.asset_files[start_index:end_index]):
            asset_path = os.path.join('assets/', asset_file)
            pixmap = QPixmap(asset_path).scaled(300, 300, Qt.KeepAspectRatio)  # Double the size of thumbnails
            asset_label = QLabel()
            asset_label.setPixmap(pixmap)
            asset_label.setAlignment(Qt.AlignCenter)
            asset_label.setFixedSize(QSize(350, 350))  # Set the size of each grid item
            asset_label.setStyleSheet("border: 1px solid #ccc; padding: 10px;")
            asset_label.setToolTip(asset_file)

            # Set the asset file as data so we can identify it on click
            asset_label.asset_file = asset_file

            # Handle click event
            asset_label.mousePressEvent = lambda event, file=asset_file: self.show_asset_preview(file)

            # Add the asset to the grid layout (2 columns, 3 rows visible at a time)
            self.asset_grid_layout.addWidget(asset_label, idx // 2, idx % 2)  # 2 columns per row

        # Update the current page display
        self.page_number_input.setText(str(self.current_page + 1))

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

    def next_page(self):
        """Navigates to the next page of assets."""
        if (self.current_page + 1) * ASSETS_PER_PAGE < self.total_assets:
            self.current_page += 1
            self.display_assets()

    def prev_page(self):
        """Navigates to the previous page of assets."""
        if self.current_page > 0:
            self.current_page -= 1
            self.display_assets()

    def jump_to_page(self):
        """Jump to the page specified by the user in the page number input."""
        try:
            page_number = int(self.page_number_input.text()) - 1
            if 0 <= page_number < self.get_total_pages():
                self.current_page = page_number
                self.display_assets()
        except ValueError:
            pass  # Ignore invalid input

    def update_total_pages(self):
        """Updates the total pages label based on the number of assets."""
        total_pages = self.get_total_pages()
        self.total_pages_label.setText(f"/ {total_pages}")

    def get_total_pages(self):
        """Returns the total number of pages based on the number of assets."""
        return max(1, (self.total_assets + ASSETS_PER_PAGE - 1) // ASSETS_PER_PAGE)

    def eventFilter(self, obj, event):
        """Event filter to dynamically resize grid items based on window size."""
        if event.type() == QEvent.Resize:
            self.resize_asset_grid()
        return super().eventFilter(obj, event)

    def resize_asset_grid(self):
        """Resize the asset grid items based on the window size."""
        available_width = self.size().width() * 0.6  # 60% of the window width
        available_height = self.size().height() * 0.8  # 80% of the window height

        # Calculate optimal size for grid items (2 columns, 3 rows visible)
        grid_item_width = available_width / 2 - 20
        grid_item_height = available_height / 3 - 20

        for i in range(self.asset_grid_layout.count()):
            widget = self.asset_grid_layout.itemAt(i).widget()
            if widget:
                widget.setFixedSize(QSize(grid_item_width, grid_item_height))

if __name__ == "__main__":
    app = QApplication([])

    window = AssetBrowser()
    window.show()

    app.exec_()
