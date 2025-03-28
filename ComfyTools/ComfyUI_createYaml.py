import os
import yaml
from collections import OrderedDict

# Define base paths
ssd_path = "/Volumes/MySSD/ComfyUI/models"
comfyui_path = os.path.expanduser("~/Projects/ComfyUI")  # Expand `~` to full path
comfyui_library = os.path.expanduser("~/Library/Application Support/ComfyUI")  # Library path
models_path = os.path.join(comfyui_path, "models")

# YAML file path
yaml_file_path = os.path.join(comfyui_library, "extra_models_config.yaml")  # Save in Library path

# Initialize ordered YAML data with the provided additional structure
yaml_data = OrderedDict({
    "comfyui_desktop": OrderedDict({
        "is_default": "true",
        "custom_nodes": "custom_nodes/",
        "download_model_base": "models",
        "base_path": comfyui_path,
    }),
    "desktop_extensions": OrderedDict({
        "custom_nodes": "/Applications/ComfyUI.app/Contents/Resources/ComfyUI/custom_nodes",
    }),
})

# Add new folder entries to the comfyui_desktop section
if os.path.exists(models_path) and os.path.isdir(models_path):
    for folder_name in sorted(os.listdir(models_path)):  # Sort folder names for consistent order
        folder_path = os.path.join(models_path, folder_name)
        if os.path.isdir(folder_path):  # Check if it's a directory
            yaml_data["comfyui_desktop"][folder_name] = f"{ssd_path}/{folder_name}"
            print(f"Added entry: {folder_name} -> {ssd_path}/{folder_name}")

# Convert nested OrderedDicts into plain dictionaries
def convert_to_dict(data):
    if isinstance(data, OrderedDict):
        return {k: convert_to_dict(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_dict(i) for i in data]
    else:
        return data

# Ensure the Library path exists
os.makedirs(comfyui_library, exist_ok=True)

# Write the YAML data to the file with proper formatting
with open(yaml_file_path, "w") as yaml_file:
    yaml.dump(convert_to_dict(yaml_data), yaml_file, default_flow_style=False, sort_keys=False)

print(f"Updated YAML file written to: {yaml_file_path}")
