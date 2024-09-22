#from qtpy.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore
import json
import os

class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setWindowTitle("User Login")

        # Get the default username (OS username or computer name)
        default_username = self.get_default_username()

        # Username and Password input fields
        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()
        self.input_username.setText(default_username)  # Pre-fill with default username

        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        # Login and Cancel buttons
        self.button_login = QPushButton("Login")
        self.button_login.clicked.connect(self.check_credentials)

        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.clicked.connect(self.reject)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.button_login)
        buttons_layout.addWidget(self.button_cancel)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def get_default_username(self):
        """Get the default username (either OS username or computer name)."""
        try:
            # Try getting the username of the logged-in user
            username = os.getlogin()
        except Exception:
            # If that fails, fallback to the computer's hostname
            username = os.environ.get('USERNAME') or os.environ.get('COMPUTERNAME')
        return username

    def check_credentials(self):
        # Load users from a JSON file
        json_file = os.path.join(os.path.dirname(__file__), "users.json")

        try:
            with open(json_file, "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Users database not found.")
            return

        username = self.input_username.text()
        password = self.input_password.text()

        # Check credentials
        if username in users and users[username] == password:
            QMessageBox.information(self, "Success", "Login Successful!")
            self.accept()  # Close the login window
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")
