import os
import json
from json_processor import load_json_metadata

class AssetHelper:
    def __init__(self):
        self.asset_tags = {}  # Dictionary to hold tags for each asset

    def load_assets(self, folder_paths):
        """Load image assets from the selected folders and their subfolders."""
        asset_files = []
        for folder_path in folder_paths:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        asset_file_path = os.path.join(root, file)
                        asset_files.append(asset_file_path)

                        # Extract tags and store them in a local file
                        json_file_path = f"{os.path.splitext(asset_file_path)[0]}versioninfo.json"
                        _, _, hashtags = load_json_metadata(json_file_path)
                        self.asset_tags[asset_file_path] = hashtags  # Store hashtags

        # Optionally, save hashtags to a local file for persistent storage
        with open("asset_tags.json", "w") as f:
            json.dump(self.asset_tags, f)

        return asset_files

    def update_tags(self, asset_files):
        """Update tags for the loaded assets based on their corresponding JSON files."""
        self.asset_tags.clear()  # Clear previous tags
        for asset_file in asset_files:
            json_file_path = f"{os.path.splitext(asset_file)[0]}versioninfo.json"
            if os.path.exists(json_file_path):
                _, _, hashtags = load_json_metadata(json_file_path)
                self.asset_tags[asset_file] = hashtags  # Store hashtags for the asset

    def filter_assets(self, search_term, tag_term, asset_files):
        """Filter assets based on search term and tags."""
        search_term = search_term.lower()
        tag_terms = [tag.strip().lower() for tag in tag_term.split(",")] if tag_term else []
        filtered_assets = []

        for asset in asset_files:
            asset_name = os.path.basename(asset).lower()
            tags = self.asset_tags.get(asset, [])

            # Check if both search term and all tags match
            if (search_term in asset_name or not search_term) and all(tag in tags for tag in tag_terms):
                filtered_assets.append(asset)

        return filtered_assets
