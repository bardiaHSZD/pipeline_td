import os
from PySide6.QtWidgets import QGroupBox, QGridLayout, QScrollArea, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize, Qt

ASSETS_PER_PAGE = 12

class AssetGrid:
    def __init__(self):
        self.asset_grid_group = QGroupBox("Assets")
        self.asset_grid_layout = QGridLayout()
        self.asset_grid_group.setLayout(self.asset_grid_layout)

        # Scroll area for assets (initially showing only 3x2 grid)
        self.asset_scroll = QScrollArea()
        self.asset_scroll.setWidgetResizable(True)
        self.asset_scroll.setWidget(self.asset_grid_group)

        self.selected_label = None  # To keep track of the selected thumbnail

    def load_assets(self, assets, start_index, end_index, parent):
        """Loads and displays assets from start_index to end_index."""
        # Clear the grid layout before loading new assets
        for i in reversed(range(self.asset_grid_layout.count())):
            widget = self.asset_grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Reset the selected label as we are reloading the grid
        self.selected_label = None

        # Load and display each asset on the current page
        for idx, asset_file in enumerate(assets[start_index:end_index]):
            asset_path = os.path.join(asset_file)
            if not os.path.exists(asset_path):
                continue  # Skip if the image file doesn't exist

            pixmap = QPixmap(asset_path)
            if pixmap.isNull():
                print(f"Error loading image: {asset_path}")
                continue  # Skip if the pixmap couldn't be loaded

            pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)

            asset_label = QLabel()
            asset_label.setPixmap(pixmap)
            asset_label.setAlignment(Qt.AlignCenter)
            asset_label.setFixedSize(QSize(350, 350))
            asset_label.setStyleSheet("border: 1px solid #ccc; padding: 10px;")
            asset_label.setToolTip(asset_file)

            # Set the asset file as data so we can identify it on click
            asset_label.asset_file = asset_file

            # Handle click event
            asset_label.mousePressEvent = lambda event, label=asset_label: self.select_asset(label, parent)

            # Add the asset to the grid layout (2 columns, 3 rows visible at a time)
            self.asset_grid_layout.addWidget(asset_label, idx // 2, idx % 2)

    def select_asset(self, label, parent):
        """Handles the selection of an asset."""
        # Check if the previously selected label is valid and exists
        if self.selected_label and self.selected_label is not label:
            # Reset the border of the previously selected thumbnail
            try:
                self.selected_label.setStyleSheet("border: 1px solid #ccc; padding: 10px;")
            except RuntimeError:
                self.selected_label = None

        # Set the border of the new selected thumbnail to orange
        label.setStyleSheet("border: 3px solid orange; padding: 10px;")
        self.selected_label = label

        # Display the selected asset in the preview section
        parent.show_asset_preview(label.asset_file)
