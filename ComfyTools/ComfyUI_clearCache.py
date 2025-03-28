import os
import shutil

# Base path for "Library/Application Support/ComfyUI"
base_path = os.path.expanduser("~/Library/Application Support/ComfyUI")

# List of subdirectories under the base path
paths = [
    "DawnGraphiteCache",
    "GPUCache",
    "Cache",
    "Network Persistent State",
    "DawnWebGPUCache",
    "Code Cache",
]

# Function to delete files and folders under the specified path
def clean_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for name in files:
            file_path = os.path.join(root, name)
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        for name in dirs:
            dir_path = os.path.join(root, name)
            shutil.rmtree(dir_path)
            print(f"Deleted folder: {dir_path}")

# Iterate over the subdirectories and clean them
for sub_path in paths:
    full_path = os.path.join(base_path, sub_path)  # Dynamically resolve the full path
    if os.path.exists(full_path):
        clean_directory(full_path)
    else:
        print(f"Path not found: {full_path}")

print("Cleanup completed.")
