import json
import os

def load_json_metadata(json_file_path):
    """Load metadata from the specified JSON file."""
    if not os.path.exists(json_file_path):
        return "N/A", "N/A", []  # Return default values if the file does not exist

    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    version = data.get("version", "N/A")  # Get the version
    global_path = data.get("locations", {}).get("global", "")
    extension = os.path.splitext(global_path)[1] if global_path else "N/A"  # Get the file extension from global path
    hashtags = data.get("comment", "").split(",")  # Extract hashtags

    # Strip whitespaces and convert to lowercase
    hashtags = [tag.strip().lower() for tag in hashtags]
    return version, extension, hashtags
