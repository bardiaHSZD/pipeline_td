from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt  # Import Qt for alignment

ASSETS_PER_PAGE = 12

class Pagination:
    def __init__(self, asset_grid, parent):
        self.asset_grid = asset_grid
        self.parent = parent

        self.layout = QHBoxLayout()

        # Pagination controls
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.prev_page)

        self.page_number_input = QLineEdit()
        self.page_number_input.setFixedWidth(40)
        self.page_number_input.setAlignment(Qt.AlignCenter)  # Use Qt.AlignCenter for alignment
        self.page_number_input.setText(str(self.parent.current_page + 1))
        self.page_number_input.returnPressed.connect(self.jump_to_page)

        self.total_pages_label = QLabel("/ 1")

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)

        # Add widgets to the layout
        self.layout.addWidget(self.prev_button)
        self.layout.addWidget(QLabel("Page:"))
        self.layout.addWidget(self.page_number_input)
        self.layout.addWidget(self.total_pages_label)
        self.layout.addWidget(self.next_button)

    def prev_page(self):
        if self.parent.current_page > 0:
            self.parent.current_page -= 1
            self.update_grid()

    def next_page(self):
        if (self.parent.current_page + 1) * ASSETS_PER_PAGE < self.parent.total_assets:
            self.parent.current_page += 1
            self.update_grid()

    def jump_to_page(self):
        """Jump to the page specified by the user in the page number input."""
        try:
            page_number = int(self.page_number_input.text()) - 1
            if 0 <= page_number < self.get_total_pages():
                self.parent.current_page = page_number
                self.update_grid()
        except ValueError:
            pass  # Ignore invalid input

    def update_grid(self):
        """Update the grid view to display assets for the current page."""
        start_index = self.parent.current_page * ASSETS_PER_PAGE
        end_index = min(start_index + ASSETS_PER_PAGE, self.parent.total_assets)
        self.asset_grid.load_assets(self.parent.asset_files, start_index, end_index, self.parent)
        self.page_number_input.setText(str(self.parent.current_page + 1))
        self.total_pages_label.setText(f"/ {self.get_total_pages()}")

    def get_total_pages(self):
        """Returns the total number of pages based on the number of assets."""
        return max(1, (self.parent.total_assets + ASSETS_PER_PAGE - 1) // ASSETS_PER_PAGE)
