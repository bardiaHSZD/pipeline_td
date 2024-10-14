from PySide6.QtWidgets import QHBoxLayout, QPushButton, QLabel, QLineEdit
from PySide6.QtCore import Qt


class Pagination:
    def __init__(self, asset_grid, parent):
        self.asset_grid = asset_grid
        self.parent = parent

        self.items_per_page = 12 #items per page (4 rows x 3 columns)
        self.layout = QHBoxLayout()

        # Previous button
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.prev_page)
        self.layout.addWidget(self.prev_button)

        # Page number input and label
        self.page_number_input = QLineEdit()
        self.page_number_input.setFixedWidth(30)
        self.page_number_input.setAlignment(Qt.AlignCenter)
        self.page_number_input.setText(str(parent.current_page + 1))  # Start with page 1
        self.page_number_input.returnPressed.connect(self.jump_to_page)
        self.layout.addWidget(self.page_number_input)

        # Page number label (total pages)
        self.page_total_label = QLabel("/ 1")
        self.layout.addWidget(self.page_total_label)

        # Next button
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        self.layout.addWidget(self.next_button)

        # Disable navigation buttons if there are no pages
        self.update_buttons()

    def update_buttons(self):
        """Update the state of the previous and next buttons based on the current page."""
        total_pages = self.get_total_pages()
        current_page = self.parent.current_page

        # Disable previous button on the first page
        self.prev_button.setDisabled(current_page == 0)

        # Disable next button on the last page
        self.next_button.setDisabled(current_page >= total_pages - 1)

        # Update the page number input and total page label
        self.page_number_input.setText(str(current_page + 1))
        self.page_total_label.setText(f"/ {total_pages}")

    def get_total_pages(self):
        """Calculate the total number of pages based on the number of assets and items per page."""
        if self.parent.total_assets == 0:
            return 1  # Default to 1 if no assets
        return (self.parent.total_assets + self.items_per_page - 1) // self.items_per_page

    def update_grid(self):
        """Update the asset grid for the current page."""
        start_index = self.parent.current_page * self.items_per_page
        end_index = min(start_index + self.items_per_page, self.parent.total_assets)

        # Load assets for the current page
        self.parent.load_assets_in_chunks(start_index, end_index)

        # Update pagination buttons
        self.update_buttons()

    def prev_page(self):
        """Go to the previous page of assets."""
        if self.parent.current_page > 0:
            self.parent.current_page -= 1
            self.update_grid()

    def next_page(self):
        """Go to the next page of assets."""
        if self.parent.current_page < self.get_total_pages() - 1:
            self.parent.current_page += 1
            self.update_grid()

    def jump_to_page(self):
        """Jump to a specific page based on the input."""
        try:
            page_number = int(self.page_number_input.text()) - 1
            if 0 <= page_number < self.get_total_pages():
                self.parent.current_page = page_number
                self.update_grid()
            else:
                self.update_buttons()  # Reset to the current valid page if the input is invalid
        except ValueError:
            self.update_buttons()  # Reset if the input is not a valid number
