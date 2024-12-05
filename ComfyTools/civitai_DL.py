import argparse
from datetime import datetime, timedelta

import requests


def human_readable_size(size_kb):
    if size_kb >= 1024**2:
        return f"{size_kb / 1024**2:.2f} GB"
    elif size_kb >= 1024:
        return f"{size_kb / 1024:.2f} MB"
    else:
        return f"{size_kb:.2f} KB"


def process_files(
    files,
    model_name,
    model_id,
    base_model,
    base_model_type,
    published_date,
    nsfw_level,
    counter,
):
    for file in files:
        if (
            file["virusScanResult"] == "Success"
            and file["metadata"]["format"] == "SafeTensor"
        ):
            counter += 1
            size_human_readable = human_readable_size(file["sizeKB"])
            print(f"{counter}. Model Name: {model_name}")
            print(f"   Model ID: {model_id}")
            print(f"   Base Model: {base_model}")
            print(f"   Base Model Type: {base_model_type}")
            print(f"   Published At: {published_date.strftime('%m/%d/%Y')}")
            print(f"   NSFW Level: {nsfw_level}")
            print(f"   SHA256: {file['hashes']['SHA256']}")
            print(f"   File Name: {file['name']}")
            print(f"   File Size: {size_human_readable}")
            print(f"   File Type: {file['type']}")
            print(f"   File Download URL: {file['downloadUrl']}")
            print("---")
    return counter


def process_models(models, counter, three_months_ago):
    for model in models:
        model_name = model.get("name", "Unknown")
        model_id = model.get("id", "Unknown")
        base_model = model.get("baseModel", "Unknown")
        base_model_type = model.get("baseModelType", "Unknown")
        nsfw_level = model.get("nsfwLevel", "Unknown")

        # Check if publishedAt key exists
        if "publishedAt" in model:
            # Parse the publishedAt date
            published_date_str = model["publishedAt"].rstrip("Z")
            try:
                published_date = datetime.strptime(
                    published_date_str, "%Y-%m-%dT%H:%M:%S.%f"
                )
            except ValueError:
                try:
                    published_date = datetime.strptime(
                        published_date_str, "%Y-%m-%dT%H:%M:%S"
                    )
                except ValueError as e:
                    print(f"Date parsing error: {e}")
                    continue

            # Check the criteria
            if published_date >= three_months_ago:
                counter = process_files(
                    model["files"],
                    model_name,
                    model_id,
                    base_model,
                    base_model_type,
                    published_date,
                    nsfw_level,
                    counter,
                )

        # Process modelVersions if they exist
        if "modelVersions" in model:
            for version in model["modelVersions"]:
                version_name = version.get("name", "Unknown")
                version_id = version.get("id", "Unknown")
                version_base_model = version.get("baseModel", base_model)
                version_base_model_type = version.get("baseModelType", base_model_type)
                version_nsfw_level = version.get("nsfwLevel", nsfw_level)

                if "publishedAt" in version:
                    published_date_str = version["publishedAt"].rstrip("Z")
                    try:
                        published_date = datetime.strptime(
                            published_date_str, "%Y-%m-%dT%H:%M:%S.%f"
                        )
                    except ValueError:
                        try:
                            published_date = datetime.strptime(
                                published_date_str, "%Y-%m-%dT%H:%M:%S"
                            )
                        except ValueError as e:
                            print(f"Date parsing error: {e}")
                            continue

                    # Check the criteria
                    if published_date >= three_months_ago:
                        counter = process_files(
                            version["files"],
                            version_name,
                            version_id,
                            version_base_model,
                            version_base_model_type,
                            published_date,
                            version_nsfw_level,
                            counter,
                        )

    return counter


def main(api_key):
    BASE_URL = "https://civitai.com/api/v1/models"
    TIMEOUT = 10  # Timeout in seconds
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    # Define the date three months ago from today
    three_months_ago = datetime.now() - timedelta(days=3 * 30)

    try:
        # Fetch models
        response = requests.get(BASE_URL, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()  # Raise an exception for HTTP errors
        models = response.json()

        counter = 0

        # Process main models and their versions
        counter = process_models(models["items"], counter, three_months_ago)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and verify models")
    parser.add_argument("--api_key", type=str, required=True, help="CivitAI API key")
    args = parser.parse_args()
    main(args.api_key)
