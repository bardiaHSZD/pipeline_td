from PySide6.QtWidgets import QScrollArea, QGridLayout, QLabel, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer


class AssetGrid:
    def __init__(self, parent):
        self.parent = parent  # The main window containing the progress bar
        self.asset_scroll = QScrollArea()
        self.asset_scroll.setWidgetResizable(True)

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.asset_scroll.setWidget(self.grid_widget)

        self.selected_label = None  # Track the selected asset label

    def load_assets(self, asset_files, start_index, end_index, parent):
        """Load the assets into the grid view with 4 rows and 3 columns (12 items per page)."""
        # Clear previous items from the grid
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Reset the selected label as we're reloading the grid
        self.selected_label = None

        total_items = end_index - start_index

        # Prepare the progress bar
        total_to_load = min(12, total_items)
        self.parent.progress_bar.setValue(0)
        self.parent.progress_bar.setMaximum(total_to_load)
        self.parent.progress_bar.setVisible(True)

        def load_item(index, row, col):
            """Helper function to load one asset at a time."""
            if index < total_items:
                asset_file = asset_files[start_index + index]
                pixmap = QPixmap(asset_file).scaled(200, 200, Qt.KeepAspectRatio)
                asset_label = QLabel()
                asset_label.setPixmap(pixmap)
                asset_label.setStyleSheet("border: none; padding: 10px;")
                asset_label.mousePressEvent = lambda event, af=asset_file, label=asset_label: self.select_asset(af, label, parent)
            else:
                asset_label = QLabel()
                asset_label.setStyleSheet("border: none; padding: 10px;")
                asset_label.setFixedSize(200, 200)

            # Add the asset label to the grid with alignment to the center
            self.grid_layout.addWidget(asset_label, row, col, alignment=Qt.AlignCenter)

            # Update row and column for next item (3 columns per row)
            col += 1
            if col == 3:
                col = 0
                row += 1

            # Update progress bar
            self.parent.progress_bar.setValue(index + 1)

            # Load next item with a slight delay to simulate progress
            if index + 1 < 12:
                QTimer.singleShot(50, lambda: load_item(index + 1, row, col))
            else:
                self.parent.progress_bar.setValue(total_to_load)  # Set to 100% when done

        load_item(0, 0, 0)

    def select_asset(self, asset_file, label, parent):
        """Select an asset and display it in the preview. Update border color for the selected asset."""
        if self.selected_label:
            self.selected_label.setStyleSheet("border: none; padding: 10px;")  # Reset previous selection

        label.setStyleSheet("border: 2px solid orange; padding: 10px;")  # Highlight selected asset
        self.selected_label = label
        parent.show_asset_preview(asset_file)
