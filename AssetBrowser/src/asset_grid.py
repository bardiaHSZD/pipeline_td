from PySide6.QtWidgets import QScrollArea, QGridLayout, QLabel, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class AssetGrid:
    def __init__(self, parent):
        self.parent = parent
        self.asset_scroll = QScrollArea()
        self.asset_scroll.setWidgetResizable(True)

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.asset_scroll.setWidget(self.grid_widget)

        self.selected_label = None

    def load_assets(self, asset_files, start_index, end_index, parent):
        """Load assets into the grid view."""
        # Clear the grid before loading new assets
        self.clear_grid()

        # Maximum 3 columns per row and 4 rows per page (12 items per page)
        max_cols = 3  # 3 columns
        max_rows = 4  # 4 rows (for a total of 12 items per page)
        total_items = end_index - start_index

        # Loop through the assets and add them to the grid
        for index in range(total_items):
            if start_index + index < len(asset_files):
                asset_file = asset_files[start_index + index]

                # Calculate the current row and column based on the index
                row = index // max_cols
                col = index % max_cols

                # Create and add the QLabel for each asset
                pixmap = QPixmap(asset_file).scaled(200, 200, Qt.KeepAspectRatio)
                asset_label = QLabel()
                asset_label.setPixmap(pixmap)
                asset_label.setStyleSheet("border: none; padding: 10px;")
                asset_label.mousePressEvent = lambda event, af=asset_file, label=asset_label: self.select_asset(af, label, parent)

                # Add the asset label to the grid at the calculated row and column
                self.grid_layout.addWidget(asset_label, row, col, alignment=Qt.AlignCenter)

    def clear_grid(self):
        """Remove all items from the grid layout."""
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def select_asset(self, asset_file, label, parent):
        """Select an asset and highlight it."""
        if self.selected_label:
            self.selected_label.setStyleSheet("border: none; padding: 10px;")

        self.selected_label = label
        label.setStyleSheet("border: 2px solid orange; padding: 10px;")
        parent.show_asset_preview(asset_file)
