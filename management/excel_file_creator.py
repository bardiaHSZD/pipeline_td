import pandas as pd

# Function to create the DataFrame for project info
def create_project_info_df():
    project_info = {
        "project_name": ["MyProject"] * 12,
        "entity_name": ["Character01", "Character01", "Character01", "Character01",
                        "Prop01", "Prop01", "Prop01", "Prop01",
                        "Vehicle01", "Vehicle01", "Vehicle01", "Vehicle01"],
        "department": ["mod", "surf", "rig", "cpt",
                       "mod", "surf", "rig", "cpt",
                       "mod", "surf", "rig", "cpt"],
        "task": ["ModelingTask01", "SurfacingTask01", "RiggingTask01", "CaptureTask01",
                 "ModelingTask02", "SurfacingTask02", "RiggingTask02", "CaptureTask02",
                 "ModelingTask01", "SurfacingTask01", "RiggingTask01", "CaptureTask01"]
    }
    return pd.DataFrame(project_info)

# Function to create the DataFrame for entities
def create_entities_df():
    entities = {
        "entity_name": ["Character01", "Character01", "Character01", "Character01",
                        "Prop01", "Prop01", "Prop01", "Prop01",
                        "Vehicle01", "Vehicle01", "Vehicle01", "Vehicle01"],
        "department": ["mod", "surf", "rig", "cpt",
                       "mod", "surf", "rig", "cpt",
                       "mod", "surf", "rig", "cpt"],
        "task": ["ModelingTask01", "SurfacingTask01", "RiggingTask01", "CaptureTask01",
                 "ModelingTask02", "SurfacingTask02", "RiggingTask02", "CaptureTask02",
                 "ModelingTask01", "SurfacingTask01", "RiggingTask01", "CaptureTask01"]
    }
    return pd.DataFrame(entities)

# Function to create the DataFrame for sequences and shots
def create_sequences_df():
    sequences = {
        "sequence_name": ["sequence_01"] * 18 + ["sequence_02"] * 18,
        "shot_name": ["shot_01"] * 6 + ["shot_02"] * 6 + ["shot_03"] * 6 + 
                     ["shot_01"] * 6 + ["shot_02"] * 6 + ["shot_03"] * 6,
        "department": ["anm", "cfx", "cmp", "fx", "lay", "lgt"] * 6,
        "task": ["AnimationTask01", "CharacterFXTask01", "CompositingTask01", "FXTask01", "LayoutTask01", "LightingTask01",
                 "AnimationTask02", "CharacterFXTask02", "CompositingTask02", "FXTask02", "LayoutTask02", "LightingTask02",
                 "AnimationTask01", "CharacterFXTask01", "CompositingTask01", "FXTask01", "LayoutTask01", "LightingTask01",
                 "AnimationTask02", "CharacterFXTask02", "CompositingTask02", "FXTask02", "LayoutTask02", "LightingTask02",
                 "AnimationTask01", "CharacterFXTask01", "CompositingTask01", "FXTask01", "LayoutTask01", "LightingTask01",
                 "AnimationTask02", "CharacterFXTask02", "CompositingTask02", "FXTask02", "LayoutTask02", "LightingTask02"]
    }
    return pd.DataFrame(sequences)

# Function to write the data to an Excel file
def write_to_excel(file_path):
    # Create DataFrames
    project_info_df = create_project_info_df()
    entities_df = create_entities_df()
    sequences_df = create_sequences_df()

    # Write DataFrames to an Excel file with multiple sheets
    with pd.ExcelWriter(file_path) as writer:
        project_info_df.to_excel(writer, sheet_name='ProjectInfo', index=False)
        entities_df.to_excel(writer, sheet_name='Entities', index=False)
        sequences_df.to_excel(writer, sheet_name='Sequences', index=False)

# File path for the output Excel file
output_file_path = 'project_structure.xlsx'

# Generate the Excel file
write_to_excel(output_file_path)

# Print the output file path
print(f"Excel file generated at: {output_file_path}")
