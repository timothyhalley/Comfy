import os
from datetime import datetime

import yaml

# Define base path and model folder
base_path = "/Users/I850916/Projects/ComfyUI"
download_model_base = "models"
complete_path = os.path.join(base_path, download_model_base)

# Define the fixed entries
fixed_entries = [
    ("is_default", "true"),
    ("custom_nodes", "custom_nodes/"),
    ("download_model_base", "models"),
    ("base_path", base_path),
]

# Initialize the YAML structure
yaml_data = {
    "comfyui_desktop": {},
    "desktop_extensions": {
        "custom_nodes": "/Applications/ComfyUI.app/Contents/Resources/ComfyUI/custom_nodes"
    },
}

# Add the fixed entries to comfyui_desktop
for key, value in fixed_entries:
    yaml_data["comfyui_desktop"][key] = value

# Add new entries for each folder under the models directory
if os.path.exists(complete_path) and os.path.isdir(complete_path):
    for folder_name in os.listdir(complete_path):
        folder_path = os.path.join(complete_path, folder_name)
        if os.path.isdir(folder_path):  # Check if it's a directory
            new_entry_key = folder_name
            new_entry_value = f"/Volumes/MySSD/ComfyUI/models/{folder_name}"
            # Add the new entry if it doesn't already exist
            if new_entry_key not in yaml_data["comfyui_desktop"]:
                yaml_data["comfyui_desktop"][new_entry_key] = new_entry_value

# Generate the file name using the current date
current_date = datetime.now().strftime("%m%d")  # Get MMDD format
file_name = f"extra_models_config_{current_date}.yaml"

# Write the YAML data to the file
with open(file_name, "w") as yaml_file:
    yaml.dump(yaml_data, yaml_file, default_flow_style=False)

print(f"YAML file written to: {file_name}")
