"""
This module is for downloading data from Hugging Face.
"""

import argparse
import hashlib
import json
import os

from huggingface_hub import hf_hub_download, login, snapshot_download

BASE_PATH = "/Volumes/MySSD/ComfyUI"


def replace_base_path(data, base_path):
    """
    Replaces the {BASE_PATH} placeholder in the model directory paths with the actual base path.

    Args:
        data (dict): Dictionary containing model information.
        base_path (str): The base path to replace the placeholder with.

    Returns:
        dict: Updated dictionary with the base path replaced.
    """
    for model_info in data["models"]:
        if "{BASE_PATH}" in model_info["dir"]:
            model_info["dir"] = model_info["dir"].replace("{BASE_PATH}", base_path)
    return data


def calculate_checksum(file_path, hash_algo="sha256"):
    """
    Calculates the checksum of a file.

    Args:
        file_path (str): Path to the file.
        hash_algo (str): Hashing algorithm to use (default is sha256).

    Returns:
        str: Calculated checksum of the file.
    """
    try:
        hash_func = hashlib.new(hash_algo)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Error calculating checksum for {file_path}: {e}")
        return None


def check_local_files(
    model_name, model_url, output_dir, filename, expected_checksum, newname=None
):
    """
    Checks if the local file exists and verifies its checksum.

    Args:
        model_name (str): Name of the model.
        model_url (str): URL of the model on Hugging Face.
        output_dir (str): Directory where the file is expected to be.
        filename (str): Original filename of the model.
        expected_checksum (str): Expected checksum of the file.
        newname (str, optional): New name for the file.

    Returns:
        bool: True if the file exists and checksum matches, False otherwise.
    """
    meaningful_filename = newname if newname else filename
    file_path = os.path.join(output_dir, meaningful_filename)

    print(f"🔍 Checking {model_name} ({model_url})...")
    if os.path.exists(file_path):
        print(f"\t📁 File exists: {meaningful_filename}")
        current_checksum = calculate_checksum(file_path)
        if current_checksum == expected_checksum:
            print(f"\t✅ Checksum matches: {meaningful_filename}")
            return True
        else:
            print(f"\t❌ Checksum mismatch: {meaningful_filename}")
            return False
    else:
        print(f"\t⚠️ File does not exist: {meaningful_filename}")
        return False


def download_and_verify(
    model_name,
    model_url,
    output_dir,
    revision_sub,
    filename,
    expected_checksum,
    newname=None,
    local_only=False,
):
    """
    Downloads a model file from Hugging Face and verifies its checksum. Renames the file if newname is provided.

    Args:
        model_name (str): Name of the model.
        model_url (str): URL of the model on Hugging Face.
        output_dir (str): Directory to save the downloaded file.
        revision_sub (str): Revision of the model.
        filename (str): Original filename of the model.
        expected_checksum (str): Expected checksum of the file.
        newname (str, optional): New name for the downloaded file.
        local_only (bool): If True, only check local files without downloading.

    Raises:
        ValueError: If the calculated checksum does not match the expected checksum.
    """
    if local_only:
        if check_local_files(
            model_name, model_url, output_dir, filename, expected_checksum, newname
        ):
            return

    try:
        meaningful_filename = newname if newname else filename
        file_path = os.path.join(output_dir, meaningful_filename)

        if os.path.exists(file_path):
            current_checksum = calculate_checksum(file_path)
            if current_checksum == expected_checksum:
                print(f"{model_name}\t{model_url}:{meaningful_filename}\t👍")
                return
            else:
                raise ValueError(f"Checksum mismatch for {model_name}: {file_path}")

        print(
            f"\n{model_name}\t{model_url}:{meaningful_filename} does not exist. Downloading...\t🌎\n"
        )

        hf_hub_download(
            repo_id=model_url,
            revision=revision_sub,
            filename=filename,
            local_dir=output_dir,
        )
        os.rename(os.path.join(output_dir, filename), file_path)
        print(f"Downloaded {model_url} -- {meaningful_filename} to {file_path}")

    except (ValueError, OSError) as e:
        print(f"Error downloading or verifying {model_name}: {e}")


def download_snapshot(
    model_name, model_url, output_dir, revision_sub, local_only=False
):
    """
    Downloads a snapshot of a model from Hugging Face and moves the files to the specified output directory.

    Args:
        model_name (str): Name of the model.
        model_url (str): URL of the model on Hugging Face.
        output_dir (str): Directory to save the snapshot files.
        revision_sub (str): Revision of the model.
        local_only (bool): If True, only check local files without downloading.

    Raises:
        OSError: If there is an error creating directories or moving files.
    """
    if local_only:
        print(f"🔍 Checking snapshot for {model_name} ({model_url})...")
        return

    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        files_exist = any(
            os.path.isfile(os.path.join(output_dir, f)) for f in os.listdir(output_dir)
        )

        if files_exist:
            print(
                f"Snapshot files for {model_name} already exist in {output_dir}. Skipping download."
            )
            return

        local_path = snapshot_download(
            repo_id=model_url, local_dir=output_dir, revision=revision_sub
        )

        for root, _, files in os.walk(local_path):
            for file in files:
                new_filename = os.path.basename(file)
                old_path = os.path.join(root, file)
                new_path = os.path.join(output_dir, new_filename)
                os.rename(old_path, new_path)
                print(f"Snapshot file {new_filename} saved to: {new_path}")

    except OSError as e:
        print(f"Error downloading snapshot {model_name}: {e}")


def main(api_key, local_only):
    """
    Main function to download and verify models from Hugging Face based on the information in models.json.

    Args:
        api_key (str): Hugging Face API key.
        local_only (bool): If True, only check local files without downloading.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    print("Current Working Directory:", os.getcwd())
    print("Files in Current Directory:", os.listdir("."))

    try:
        login(token=api_key)
    except Exception as e:
        print(f"Error logging in to Hugging Face: {e}")

    json_file_path = "models.json"
    print(f"Looking for JSON file at: {json_file_path}")
    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file {json_file_path}: {e}")
        return

    data = replace_base_path(data, BASE_PATH)

    for model_info in data["models"]:
        try:
            model_name = model_info["name"]
            model_type = model_info["type"]
            model_url = model_info["url"]
            output_dir = model_info["dir"]
            revision_sub = model_info.get("revision", "main")
            newname = model_info.get("newname", None)

            os.makedirs(output_dir, exist_ok=True)

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
                    newname,
                    local_only,
                )
            elif model_type == "SNAPSHOT":
                download_snapshot(
                    model_name, model_url, output_dir, revision_sub, local_only
                )
        except KeyError as e:
            print(f"KeyError in model_info: {e}")
        except Exception as e:
            print(f"Error setting up download for {model_name}: {e}")

    print(
        "\n\nAll models and snapshots checked/downloaded to their respective directories successfully! 😎"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and verify models")
    parser.add_argument(
        "--api_key", type=str, required=True, help="Hugging Face API key"
    )
    parser.add_argument(
        "--localonly",
        action="store_true",
        help="Only check local files without downloading",
    )
    args = parser.parse_args()
    main(args.api_key, args.localonly)
