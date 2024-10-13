from PySide6.QtWidgets import QApplication
from asset_browser import AssetBrowser
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AssetBrowser()
    window.show()
    sys.exit(app.exec())


