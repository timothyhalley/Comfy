import os


def create_symlinks(source_folder, target_folder):
    # Get the list of all subfolders in the source folder
    subfolders = [f.path for f in os.scandir(source_folder) if f.is_dir()]

    for subfolder in subfolders:
        # Get the folder name
        folder_name = os.path.basename(subfolder)

        # Create the new folder name with an underscore prefix
        new_folder_name = f"~{folder_name}"

        # Create the full path for the new folder
        new_folder_path = os.path.join(source_folder, new_folder_name)

        # Rename the original folder to the new folder name
        os.rename(subfolder, new_folder_path)

        # Create the symlink pointing to the target folder
        symlink_path = os.path.join(source_folder, folder_name)
        target_path = os.path.join(target_folder, folder_name)

        os.symlink(target_path, symlink_path)
        print(f"Created symlink: {symlink_path} -> {target_path}")


# Example usage
source_folder = "/Users/timothyhalley/Projects/ComfyUI/models"
target_folder = "/Volumes/MySSD/ComfyUI/models"

create_symlinks(source_folder, target_folder)
