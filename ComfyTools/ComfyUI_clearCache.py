import os
import shutil

# List of paths to be cleaned
paths = [
    "/Users/timothyhalley/Library/Application Support/ComfyUI/DawnGraphiteCache",
    "/Users/timothyhalley/Library/Application Support/ComfyUI/GPUCache",
    "/Users/timothyhalley/Library/Application Support/ComfyUI/Cache",
    "/Users/timothyhalley/Library/Application Support/ComfyUI/Network Persistent State",
    "/Users/timothyhalley/Library/Application Support/ComfyUI/DawnWebGPUCache",
    "/Users/timothyhalley/Library/Application Support/ComfyUI/Code Cache",
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


for path in paths:
    if os.path.exists(path):
        clean_directory(path)
    else:
        print(f"Path not found: {path}")

print("Cleanup completed.")
