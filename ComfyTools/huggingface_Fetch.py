import argparse

import requests


# Function to check if the model is gated
def check_model_gated(repo_id, token, debug):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://huggingface.co/api/models/{repo_id}"
    if debug:
        print(f"🔍 Checking if model is gated: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("gated", False)
    else:
        return False


# Function to accept Terms and Conditions for a gated model
def accept_model_terms(repo_id, token, debug):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://huggingface.co/api/models/{repo_id}/terms"
    if debug:
        print(f"🔍 Accepting Terms and Conditions: {url}")
    response = requests.post(url, headers=headers)
    return response.status_code == 200


# Function to get the model card content
def get_model_card(repo_url, token, debug):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{repo_url}/raw/main/README.md"
    if debug:
        print(f"🔍 Fetching URL: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: {response.status_code}"


# Function to get the list of files in the repository
def get_repo_files(repo_url, token, debug):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{repo_url}/tree/main"
    if debug:
        print(f"📂 Fetching URL: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: {response.status_code}"


# Main function
def main():
    parser = argparse.ArgumentParser(
        description="Fetch model card and repository files from Hugging Face."
    )
    parser.add_argument("--api_key", required=True, help="Hugging Face API key")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode to print URLs being fetched",
    )
    args = parser.parse_args()

    token = args.api_key
    debug = args.debug

    repo_id = "black-forest-labs/FLUX.1-dev"
    repo_url = f"https://huggingface.co/{repo_id}"

    # Check if the model is gated and accept Terms and Conditions if necessary
    if check_model_gated(repo_id, token, debug):
        print("⚠️ Model is gated. Accepting Terms and Conditions...")
        if accept_model_terms(repo_id, token, debug):
            print("✅ Terms and Conditions accepted.")
        else:
            print("❌ Failed to accept Terms and Conditions.")
            return

    print("🔍 Fetching model card...")
    model_card = get_model_card(repo_url, token, debug)
    print("Model Card Content:")
    print(model_card)

    print("\n📂 Fetching repository files...")
    repo_files = get_repo_files(repo_url, token, debug)
    print("Repository Files:")
    print(repo_files)


if __name__ == "__main__":
    main()
