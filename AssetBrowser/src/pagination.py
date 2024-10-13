from PySide6.QtWidgets import QHBoxLayout, QPushButton, QLabel, QLineEdit

class Pagination:
    def __init__(self, asset_grid, parent):
        self.asset_grid = asset_grid
        self.parent = parent
        self.current_page = 0
        self.items_per_page = 6  # Define how many items you want per page

        # Create the pagination layout with Previous, Page Number, and Next buttons
        self.layout = QHBoxLayout()

        # Previous button
        self.previous_button = QPushButton("Previous")
        self.previous_button.clicked.connect(self.previous_page)
        self.layout.addWidget(self.previous_button)

        # Page number display
        self.page_label = QLabel(f"Page: {self.current_page + 1}")
        self.layout.addWidget(self.page_label)

        # Page number input (jump to page)
        self.page_number_input = QLineEdit()
        self.page_number_input.setFixedWidth(40)
        self.page_number_input.setText(str(self.current_page + 1))
        self.page_number_input.returnPressed.connect(self.jump_to_page)
        self.layout.addWidget(self.page_number_input)

        # Total pages label
        self.total_pages_label = QLabel(f"of {self.get_total_pages()} pages")
        self.layout.addWidget(self.total_pages_label)

        # Next button
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        self.layout.addWidget(self.next_button)

    def get_total_pages(self):
        """Calculate the total number of pages based on the total assets and items per page."""
        if self.parent.total_assets == 0:
            return 1
        return (self.parent.total_assets + self.items_per_page - 1) // self.items_per_page

    def update_grid(self):
        """Update the asset grid with assets from the current page."""
        start_index = self.current_page * self.items_per_page
        end_index = min(start_index + self.items_per_page, self.parent.total_assets)
        self.asset_grid.load_assets(self.parent.asset_files, start_index, end_index, self.parent)
        self.page_label.setText(f"Page: {self.current_page + 1}")
        self.page_number_input.setText(str(self.current_page + 1))
        self.total_pages_label.setText(f"of {self.get_total_pages()} pages")

    def next_page(self):
        """Go to the next page, if available."""
        if (self.current_page + 1) * self.items_per_page < self.parent.total_assets:
            self.current_page += 1
            self.update_grid()

    def previous_page(self):
        """Go to the previous page, if available."""
        if self.current_page > 0:
            self.current_page -= 1
            self.update_grid()

    def jump_to_page(self):
        """Jump to a specific page based on user input."""
        try:
            page_number = int(self.page_number_input.text()) - 1
            total_pages = self.get_total_pages()
            if 0 <= page_number < total_pages:
                self.current_page = page_number
                self.update_grid()
            else:
                self.page_number_input.setText(str(self.current_page + 1))  # Reset to current page if invalid input
        except ValueError:
            self.page_number_input.setText(str(self.current_page + 1))  # Reset to current page if invalid input
