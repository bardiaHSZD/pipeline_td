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

    def filter_assets(self, search_term, tag_expression, asset_files):
        """Filter assets based on search term and the parsed tag expression."""
        search_term = search_term.lower()
        filtered_assets = []

        for asset in asset_files:
            asset_name = os.path.basename(asset).lower()
            asset_tags = self.asset_tags.get(asset, [])

            # Check if the search term matches the asset name
            search_match = search_term in asset_name or not search_term

            # Check if the tags match according to the parsed expression
            tags_match = self.evaluate_tag_expression(tag_expression, asset_tags)

            # Add the asset to the results if both the search term and tag conditions are met
            if search_match and tags_match:
                filtered_assets.append(asset)

        return filtered_assets

    def evaluate_tag_expression(self, expression, asset_tags):
        """Recursively evaluate the parsed tag expression against the asset tags."""
        result = False
        for operator, operands in expression:
            if operator == 'AND':
                # AND: All operands must match
                sub_result = all(self.evaluate_operand(operand, asset_tags) for operand in operands)
            elif operator == 'OR':
                # OR: At least one operand must match
                sub_result = any(self.evaluate_operand(operand, asset_tags) for operand in operands)

            # Combine the result (AND/OR) based on the operator
            result = sub_result if result is False else (result and sub_result if operator == 'AND' else result or sub_result)
        return result

    def evaluate_operand(self, operand, asset_tags):
        """Evaluate a single operand (which could be a tag or a sub-expression)."""
        if isinstance(operand, list):
            # It's a sub-expression, so evaluate it recursively
            return self.evaluate_tag_expression(operand, asset_tags)
        else:
            # It's a tag, so check if it's in the asset tags
            return operand in asset_tags

    def update_tags(self, asset_files):
        """Update tags for the loaded assets based on their corresponding JSON files."""
        self.asset_tags.clear()  # Clear previous tags
        for asset_file in asset_files:
            json_file_path = f"{os.path.splitext(asset_file)[0]}versioninfo.json"
            if os.path.exists(json_file_path):
                _, _, hashtags = load_json_metadata(json_file_path)
                self.asset_tags[asset_file] = hashtags  # Store hashtags for the asset
