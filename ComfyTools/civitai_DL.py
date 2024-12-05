import sys

import requests


def main(api_key):
    BASE_URL = "https://civitai.com/api/v1/models"
    TIMEOUT = 10  # Timeout in seconds

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        # Fetch models
        response = requests.get(BASE_URL, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()  # Raise an exception for HTTP errors
        models = response.json()

        # Print model details and check virus scan results
        for model in models["items"]:
            print(f"Model Name: {model['name']}")
            print(f"Model ID: {model['id']}")
            print(f"Download URL: {model['downloadUrl']}")
            print("---")

            # Check files for virus scan results
            for file in model["files"]:
                if file["virusScanResult"] == "Success":
                    print(f"File {file['name']} passed virus scan.")
                    download_url = file["downloadUrl"]

                    # Download the file
                    download_response = requests.get(
                        download_url, headers=headers, timeout=TIMEOUT
                    )
                    download_response.raise_for_status()  # Raise an exception for HTTP errors

                    # Save the file
                    with open(file["name"], "wb") as f:
                        f.write(download_response.content)
                    print(f"File {file['name']} downloaded successfully!")
                else:
                    print(f"File {file['name']} failed virus scan. Skipping download.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <api_key>")
        sys.exit(1)

    api_key = sys.argv[1]
    main(api_key)
