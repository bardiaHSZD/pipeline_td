import os
import json

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
                        asset_files.append(os.path.join(root, file))

        return asset_files

    def update_tags(self, asset_files):
        """Update tags for the loaded assets based on their corresponding JSON files."""
        self.asset_tags.clear()  # Clear previous tags
        for asset_file in asset_files:
            json_file_path = f"{os.path.splitext(asset_file)[0]}versioninfo.json"
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r') as json_file:
                    data = json.load(json_file)
                    tags = data.get("comment", "").split(",")  # Assuming tags are comma-separated
                    self.asset_tags[asset_file] = [tag.strip().lower() for tag in tags]  # Store tags for the asset

    def filter_assets(self, search_term, tag_term, asset_files):
        """Filter assets based on search term and tags."""
        search_term = search_term.lower()
        tag_term = tag_term.lower()
        filtered_assets = []

        for asset in asset_files:
            asset_name = os.path.basename(asset).lower()
            tags = self.asset_tags.get(asset, [])
            if search_term in asset_name or any(tag_term in tag for tag in tags):
                filtered_assets.append(asset)

        return filtered_assets

    def filter_assets_by_search(self, all_asset_files, search_text):
        """Filter assets based on search input."""
        search_text = search_text.lower()
        matching_assets = []
        for asset in all_asset_files:
            asset_name = os.path.basename(asset).lower()
            if asset_name.startswith(search_text):
                matching_assets.append(asset)
        return matching_assets
