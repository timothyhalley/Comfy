import argparse
import hashlib
import json
import os

from huggingface_hub import hf_hub_download, login, snapshot_download

# Define the BASE_PATH constant
BASE_PATH = "/Volumes/MySSD/ComfyUI"


# Function to replace {BASE_PATH} placeholders
def replace_base_path(data, base_path):
    for model_info in data["models"]:
        if "{BASE_PATH}" in model_info["dir"]:
            model_info["dir"] = model_info["dir"].replace("{BASE_PATH}", base_path)
    return data


# Function to calculate the checksum of a file
def calculate_checksum(file_path, hash_algo="sha256"):
    try:
        hash_func = hashlib.new(hash_algo)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        print(f"Error calculating checksum: {e}")
        return None


# Function to download and verify file
def download_and_verify(
    model_name, model_url, output_dir, revision_sub, filename, expected_checksum
):
    try:
        # Extract just the file name from the provided filename path
        new_filename = os.path.basename(filename)
        file_path = os.path.join(output_dir, new_filename)

        if os.path.exists(file_path):
            # Calculate the checksum of the existing file
            current_checksum = calculate_checksum(file_path)
            if current_checksum == expected_checksum:
                print(f"{model_name}\t{model_url}:{new_filename}\t👍")
                return
            else:
                print(
                    f"\n{model_name}\t{model_url}:{new_filename} exists but checksum is incorrect.\t👎\n"
                )
                return
        else:
            print(
                f"\n{model_name}\t{model_url}:{new_filename} does not exist. Downloading...\t🌎\n"
            )

        # Download the file
        hf_hub_download(
            repo_id=model_url,
            revision=revision_sub,
            filename=filename,
            local_dir=output_dir,
        )
        os.rename(
            os.path.join(output_dir, filename), file_path
        )  # Rename the file to new filename
        print(f"Downloaded {model_url} -- {new_filename} to {file_path}")
    except Exception as e:
        print(f"Error downloading or verifying {model_name}: {e}")


# Function to download a snapshot
def download_snapshot(model_name, model_url, output_dir, revision_sub):
    try:
        local_path = snapshot_download(
            repo_id=model_url, local_dir=output_dir, revision=revision_sub
        )

        # Move and rename files within the snapshot directory
        for root, dirs, files in os.walk(local_path):
            for file in files:
                new_filename = os.path.basename(file)  # Extract just the file name
                old_path = os.path.join(root, file)
                new_path = os.path.join(output_dir, new_filename)
                os.rename(old_path, new_path)
                print(f"Snapshot file {new_filename} saved to: {new_path}")
    except Exception as e:
        print(f"Error downloading snapshot {model_name}: {e}")


def main(api_key):
    # Change the working directory to the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Debugging statements
    print("Current Working Directory:", os.getcwd())
    print("Files in Current Directory:", os.listdir("."))

    # Log in to Hugging Face
    try:
        login(token=api_key)
    except Exception as e:
        print(f"Error logging in: {e}")

    # Load the models information from models.json
    json_file_path = "models.json"
    print(f"Looking for JSON file at: {json_file_path}")
    with open(json_file_path, "r") as f:
        data = json.load(f)

    # Replace {BASE_PATH} with the actual BASE_PATH value
    data = replace_base_path(data, BASE_PATH)

    # Download each model or snapshot based on the type
    for model_info in data["models"]:
        try:
            model_name = model_info["name"]
            model_type = model_info["type"]
            model_url = model_info["url"]
            output_dir = model_info["dir"]
            revision_sub = model_info.get("revision", "main")

            os.makedirs(
                output_dir, exist_ok=True
            )  # Create directory if it doesn't exist

            if model_type == "MODEL":
                filename = model_info["filename"]
                expected_checksum = model_info["checksum"]
                download_and_verify(
                    model_name,
                    model_url,
                    output_dir,
                    revision_sub,
                    filename,
                    expected_checksum,
                )
            elif model_type == "SNAPSHOT":
                download_snapshot(model_name, model_url, output_dir, revision_sub)
        except Exception as e:
            print(f"Error setting up download for {model_name}: {e}")

    print(
        "All models and snapshots downloaded to their respective directories successfully!"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and verify models")
    parser.add_argument(
        "--api_key", type=str, required=True, help="Hugging Face API key"
    )
    args = parser.parse_args()
    main(args.api_key)
