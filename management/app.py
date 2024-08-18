import os
import json

# Load JSON data
def load_json_data(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

# Create structure for each entity based on its specific task JSON data
def create_entity_structure(entity_name, asset_tasks):
    return {
        "Exports": {},
        "Playblasts": {},
        "Renders": {},
        "Scenefiles": {
            department: {
                task: {} for task in tasks
            } for department, tasks in asset_tasks.items()
        }
    }

# Create structure for each shot based on its specific task JSON data
def create_shot_structure(shot_tasks):
    return {
        "Exports": {},
        "Playblasts": {},
        "Renders": {},
        "Scenefiles": {
            department: {
                task: {} for task in tasks
            } for department, tasks in shot_tasks.items()
        }
    }

# Define the folder structure based on the JSON data
def create_folder_structure(project_data):
    project_name = project_data['project_name']
    entities = project_data.get('entities', {})
    sequences = project_data.get('sequences', {})

    # Define the base folder structure
    folder_structure = {
        project_name: {
            "Production": {
                "Assets": {
                    "Entities": {
                        entity: create_entity_structure(entity, tasks)
                        for entity, tasks in entities.items()
                    }
                },
                "Shots": {
                    sequence: {
                        shot: create_shot_structure(shot_tasks)
                        for shot, shot_tasks in sequence_data['shots'].items()
                    } for sequence, sequence_data in sequences.items()
                }
            },
            "Pipeline": {},
            "Cache": {}
        }
    }

    return folder_structure

# Function to create folders recursively
def create_folders(structure, base_path=""):
    for key, value in structure.items():
        full_path = os.path.join(base_path, key)
        os.makedirs(full_path, exist_ok=True)
        print(f"Created directory: {full_path}")
        if isinstance(value, dict):
            create_folders(value, full_path)

# Main function
def main():
    # Check if the combined file is available
    combined_json_file = 'combined_project_structure.json'
    if os.path.exists(combined_json_file):
        project_data = load_json_data(combined_json_file)
    else:
        # Load the project structure from the separate JSON files
        project_json_file = 'sequences_shots.json'
        project_data = load_json_data(project_json_file)

        # Load individual asset and shot task files
        for entity in project_data['entities']:
            asset_tasks_file = f'asset_tasks/{entity}_tasks.json'
            project_data['entities'][entity] = load_json_data(asset_tasks_file)

        for sequence in project_data['sequences']:
            for shot in project_data['sequences'][sequence]:
                shot_tasks_file = f'shot_tasks/{sequence}/{shot}_tasks.json'
                project_data['sequences'][sequence]['shots'][shot] = load_json_data(shot_tasks_file)

    # Create the folder structure
    folder_structure = create_folder_structure(project_data)

    # Create the folders
    create_folders(folder_structure)

# Run the script
if __name__ == "__main__":
    main()
