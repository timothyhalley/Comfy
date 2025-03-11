import hashlib
import json
import os

from huggingface_hub import HfApi, login


# Function to calculate the checksum of a file
def calculate_checksum(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


# Function to create JSON entry
def create_json_entry(name, url, base_path, filename, checksum, model_type):
    newname = os.path.basename(url).replace(".safetensors", "") + ".safetensors"
    return {
        "name": name,
        "type": model_type,
        "url": url,
        "dir": f"{base_path}/models/diffusion_models/{name}",
        "revision": "main",
        "filename": filename,
        "newname": newname,
        "checksum": checksum,
    }


# Main function to read folder and search Hugging Face
def main(model_path, base_path, api_key):
    # Log in to Hugging Face
    print("🔑 Logging in to Hugging Face...")
    login(api_key)
    api = HfApi()
    json_entries = []

    for root, _, files in os.walk(model_path):
        for file in files:
            if file.endswith(".safetensors"):
                file_path = os.path.join(root, file)
                print(f"📄 Processing file: {file_path}")
                checksum = calculate_checksum(file_path)
                model_name = os.path.splitext(file)[0]

                # Search for the model on Hugging Face
                print(f"🔍 Searching for model: {model_name}")
                search_results = api.list_models(filter=model_name)
                if search_results:
                    model_info = search_results[0]
                    url = model_info.modelId
                    model_type = model_info.tags[0] if model_info.tags else "MODEL"
                    print(f"✅ Model found: {url} (Type: {model_type})")
                    json_entry = create_json_entry(
                        model_name, url, base_path, file, checksum, model_type
                    )
                    json_entries.append(json_entry)
                else:
                    print(f"❌ Model not found: {model_name}")

    # Save JSON entries to a file
    with open("models_hf.json", "w") as json_file:
        json.dump(json_entries, json_file, indent=4)
    print("💾 JSON file saved: models_hf.json")


# Example usage
if __name__ == "__main__":
    MODEL_PATH = "/path/to/your/folder"
    BASE_PATH = "/Volumes/MySSD/ComfyUI"
    API_KEY = "your_huggingface_api_key"
    main(MODEL_PATH, BASE_PATH, API_KEY)
