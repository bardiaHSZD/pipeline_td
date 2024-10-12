import os
from database import AssetDatabase

class FileCrawler:
    def __init__(self, directory):
        self.directory = directory
        self.db = AssetDatabase()

    def crawl(self):
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith(('.png', '.jpg', '.fbx', '.obj')):
                    file_path = os.path.join(root, file)
                    thumbnail_path = self.generate_thumbnail(file_path)
                    metadata = f"File size: {os.path.getsize(file_path)} bytes"
                    self.db.add_asset(file, file_path, thumbnail_path, metadata)

    def generate_thumbnail(self, file_path):
        # Placeholder for thumbnail generation logic
        return "/path/to/thumbnail.png"

    def close(self):
        self.db.close()
