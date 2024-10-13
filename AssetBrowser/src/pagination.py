from PySide6.QtWidgets import QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt


class Pagination:
    def __init__(self, asset_grid, parent):
        self.asset_grid = asset_grid
        self.parent = parent

        self.layout = QHBoxLayout()

        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.prev_page)
        self.layout.addWidget(self.prev_button)

        # Page number input (disabled as we don't want users to edit it directly)
        self.page_number_input = QLabel("1/1")  # Show the page number as label, starting at 1/1
        self.page_number_input.setAlignment(Qt.AlignCenter)  # Center the text
        self.layout.addWidget(self.page_number_input)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        self.layout.addWidget(self.next_button)

        self.update_page_label()  # Initialize the page label text

    def get_total_pages(self):
        """Calculate the total number of pages."""
        return max(1, (self.parent.total_assets + 11) // 12)  # 12 items per page

    def prev_page(self):
        """Go to the previous page."""
        if self.parent.current_page > 0:
            self.parent.current_page -= 1
            self.update_grid()

    def next_page(self):
        """Go to the next page."""
        if self.parent.current_page < self.get_total_pages() - 1:
            self.parent.current_page += 1
            self.update_grid()

    def update_grid(self):
        """Update the grid view with the current page of assets."""
        start_index = self.parent.current_page * 12
        end_index = min(self.parent.total_assets, start_index + 12)
        self.asset_grid.load_assets(self.parent.asset_files, start_index, end_index, self.parent)
        self.update_page_label()

    def update_page_label(self):
        """Update the page number display."""
        total_pages = self.get_total_pages()
        current_page = self.parent.current_page + 1  # Page is 1-indexed
        self.page_number_input.setText(f"{current_page}/{total_pages}")
