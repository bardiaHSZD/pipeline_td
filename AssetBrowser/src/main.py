from PySide6.QtWidgets import QApplication
from gui import AssetBrowser

if __name__ == "__main__":
    app = QApplication([])

    window = AssetBrowser()
    window.show()

    app.exec()  # Use app.exec() instead of app.exec_()
