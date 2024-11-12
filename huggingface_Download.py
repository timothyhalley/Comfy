import hashlib

from huggingface_hub import hf_hub_download

base_path = "/Volumes/MySSD/ComfyUI"

from huggingface_hub import hf_hub_download, login

# List of model URLs and their corresponding directories
models = {
    "Think Diffusion XL": {
        "url": "ThinkDiffusion/ThinkDiffusionXL",
        "dir": f"{base_path}/models/checkpoints/",
        "filename": "ThinkDiffusionXL.safetensors",
        "checksum": "a21c9949efcb8a0218f575aaff3fd5e8fedc508ca6757ddb44c5958cb0859f77",
    },
    "Anime Art Diffusion XL Alpha": {
        "url": "nolual/majic",
        "dir": f"{base_path}/models/checkpoints/",
        "filename": "animeArtDiffusionXL_alpha3.safetensors",
        "checksum": "53bb4fdc63b36014201f2789eab73f3b2b3569a2a9a57b3efb28d4f17283e4c4",
    },
    "SD3.5 Large": {
        "url": "stabilityai/stable-diffusion-3.5-large",
        "dir": f"{base_path}/models/checkpoints/",
        "filename": "sd3.5_large.safetensors",
        "checksum": "ffef7a279d9134626e6ce0d494fba84fc1c7e720b3c7df2d19a09dc3796d8f93",
    },
    "SD3.5 Turbo": {
        "url": "stabilityai/stable-diffusion-3.5-large-turbo",
        "dir": f"{base_path}/models/checkpoints/",
        "filename": "sd3.5_large_turbo.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "SD3.5 Medium": {
        "url": "stabilityai/stable-diffusion-3.5-medium",
        "dir": f"{base_path}/models/checkpoints/",
        "filename": "sd3.5_medium.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "SD XL Refiner 1.0": {
        "url": "stabilityai/stable-diffusion-xl-refiner-1.0",
        "dir": f"{base_path}/models/checkpoints/",
        "filename": "sd_xl_refiner_1.0_0.9vae.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "Epic Realism RC1": {
        "url": "Justin-Choo/epiCRealism-Natural_Sin_RC1_VAE",
        "dir": f"{base_path}/models/checkpoints/",
        "filename": "epicrealism_naturalSinRC1VAE.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "Photon AI": {
        "url": "WALIDALI/lcmphoton",
        "dir": f"{base_path}/models/checkpoints/",
        "filename": "photonLCM_v10.safetensors",
        "checksum": "expected_checksum_value1",
    },
    # Clip Models
    "SD3.5 Diffusion Text Encoder - G": {
        "url": "stabilityai/stable-diffusion-3-medium",
        "dir": f"{base_path}/models/clip/",
        "filename": "text_encoders/clip_g.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "SD3.5 Diffusion Text Encoder - L": {
        "url": "stabilityai/stable-diffusion-3-medium",
        "dir": f"{base_path}/models/clip/",
        "filename": "text_encoders/clip_l.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "SD3.5 Diffusion Text Encoder - FP16": {
        "url": "stabilityai/stable-diffusion-3-medium",
        "dir": f"{base_path}/models/clip/",
        "filename": "text_encoders/t5xxl_fp16.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "SDXL VAE": {
        "url": "stabilityai/sdxl-vae",
        "dir": f"{base_path}/models/vae/",
        "filename": "sdxl_vae.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "FLUX 1 DEV": {
        "url": "black-forest-labs/FLUX.1-dev",
        "dir": f"{base_path}/models/unet/",
        "filename": "flux1-dev.safetensors",
        "checksum": "expected_checksum_value1",
    },
    # XLabs-AI/flux-controlnet-collections
    "ControlNet Union Pro": {
        "url": "Shakker-Labs/FLUX.1-dev-ControlNet-Union-Pro",
        "dir": f"{base_path}/models/controlnet",
        "filename": "diffusion_pytorch_model.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "FLUX ControlNet Diff": {
        "url": "Shakker-Labs/FLUX.1-dev-ControlNet-Union-Pro",
        "dir": f"{base_path}/models/controlnet",
        "filename": "diffusion_pytorch_model.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "FLUX ControlNet Canny": {
        "url": "XLabs-AI/flux-controlnet-collections",
        "dir": f"{base_path}/models/controlnet",
        "filename": "flux-canny-controlnet-v3.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "FLUX ControlNet Depth": {
        "url": "XLabs-AI/flux-controlnet-collections",
        "dir": f"{base_path}/models/controlnet",
        "filename": "flux-depth-controlnet-v3.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "FLUX ControlNet V3": {
        "url": "XLabs-AI/flux-controlnet-collections",
        "dir": f"{base_path}/models/controlnet",
        "filename": "flux-hed-controlnet-v3.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "SD15 Monster Control": {
        "url": "monster-labs/control_v1p_sd15_qrcode_monster",
        "dir": f"{base_path}/models/controlnet",
        "filename": "v2/control_v1p_sd15_qrcode_monster_v2.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "LineArt FP16": {
        "url": "comfyanonymous/ControlNet-v1-1_fp16_safetensors",
        "dir": f"{base_path}/models/controlnet",
        "filename": "control_v11p_sd15_lineart_fp16.safetensors",
        "checksum": "expected_checksum_value1",
    },
    # VAE
    "FLUX VAE": {
        "url": "black-forest-labs/FLUX.1-schnell",
        "dir": f"{base_path}/models/vae",
        "filename": "ae.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "FLUX VAE Schnell": {
        "url": "black-forest-labs/FLUX.1-schnell",
        "dir": f"{base_path}/models/vae",
        "filename": "flux1-schnell.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "SD VAE MAE": {
        "url": "stabilityai/sd-vae-ft-mse-original",
        "dir": f"{base_path}/models/vae",
        "filename": "vae-ft-mse-840000-ema-pruned.safetensors",
        "checksum": "expected_checksum_value1",
    },
    # Lora Models
    "XL Lego Brickheadz": {
        "url": "nerijs/lego-brickheadz-xl",
        "dir": f"{base_path}/models/loras/",
        "filename": "legobrickheadz-v1.0-000004.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "LEGO Minifig XL": {
        "url": "nerijs/lego-minifig-xl",
        "dir": f"{base_path}/models/loras/",
        "filename": "legominifig-v1.0-000003.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "FLUX LoRAs Base": {
        "url": "XLabs-AI/flux-RealismLora",
        "dir": f"{base_path}/models/loras",
        "filename": "lora.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "FLUX LoRAs Anime": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": f"{base_path}/models/loras",
        "filename": "anime_lora.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "FLUX LoRAs Real": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": f"{base_path}/models/loras",
        "filename": "realism_lora.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "FLUX LoRAs Disney": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": f"{base_path}/models/loras",
        "filename": "disney_lora.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "FLUX LoRAs Scenery": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": f"{base_path}/models/loras",
        "filename": "scenery_lora.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "FLUX LoRAs MJV6": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": f"{base_path}/models/loras",
        "filename": "mjv6_lora.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "FLUX LoRAs Furry": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": f"{base_path}/models/loras",
        "filename": "furry_lora.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "Alien God SDXL": {
        "url": "CiroN2022/alien-god",
        "dir": f"{base_path}/models/loras",
        "filename": "Alien_God_sdxl.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "AnimateDiff Lora": {
        "url": "camenduru/AnimateDiff",
        "dir": f"{base_path}/models/animatediff_motion_lora",
        "filename": "v2_lora_ZoomIn.ckpt",
        "checksum": "expected_checksum_value1",
    },
    "AnimateLCM TV2 Beta": {
        "url": "wangfuyun/AnimateLCM",
        "dir": f"{base_path}/models/animatediff_motion_lora",
        "filename": "AnimateLCM_sd15_t2v_lora.safetensors",
        "checksum": "expected_checksum_value1",
    },
    # GGUF Models for FLUX
    "GGUF Unet Q6_K": {
        "url": "city96/FLUX.1-schnell-gguf",
        "dir": f"{base_path}/models/diffusion_models/FLUX1",
        "filename": "flux1-schnell-Q6_K.gguf",
        "checksum": "expected_checksum_value1",
    },
    "GGUF Unet F16": {
        "url": "city96/FLUX.1-dev-gguf",
        "dir": f"{base_path}/models/diffusion_models/FLUX1",
        "filename": "flux1-dev-F16.gguf",
        "checksum": "expected_checksum_value1",
    },
    "GGUF Unet Q80": {
        "url": "city96/FLUX.1-dev-gguf",
        "dir": f"{base_path}/models/diffusion_models/FLUX1",
        "filename": "flux1-dev-Q8_0.gguf",
        "checksum": "expected_checksum_value1",
    },
    "GGUF Encoder Q8_0": {
        "url": "city96/t5-v1_1-xxl-encoder-gguf",
        "dir": f"{base_path}/models/clip",
        "filename": "t5-v1_1-xxl-encoder-Q8_0.gguf",
        "checksum": "expected_checksum_value1",
    },
    # IP Adaptor
    "FLUX IP Adapter": {
        "url": "XLabs-AI/flux-ip-adapter-v2",
        "dir": f"{base_path}/models/ipadapter",
        "filename": "ip_adapter.safetensors",
        "checksum": "expected_checksum_value1",
    },
    "FLUX Clip Adapter": {
        "url": "openai/clip-vit-large-patch14",
        "dir": f"{base_path}/models/clip",
        "filename": "model.safetensors",
        "checksum": "expected_checksum_value1",
    },
}

# Log in to Hugging Face
login()


# Function to calculate the checksum of a file
def calculate_checksum(file_path, hash_algo="sha256"):
    hash_func = hashlib.new(hash_algo)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()


# Function to download and verify file
def download_and_verify(model_url, output_dir, filename, expected_checksum):
    file_path = os.path.join(output_dir, filename)
    if os.path.exists(file_path):
        # Calculate the checksum of the existing file
        current_checksum = calculate_checksum(file_path)
        if current_checksum == expected_checksum:
            print(f"{filename} already exists and checksum is correct.")
            return
        else:
            print(f"{filename} exists but checksum is incorrect. Redownloading...")
    else:
        print(f"{filename} does not exist. Downloading...")

    # Download the file
    hf_hub_download(repo_id=model_url, filename=filename, local_dir=output_dir)
    print(f"Downloaded {filename} to {file_path}")


# Download each model into its specified directory
for model_name, model_info in models.items():
    model_url = model_info["url"]
    output_dir = model_info["dir"]
    filename = model_info["filename"]
    expected_checksum = model_info["checksum"]
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
    download_and_verify(model_url, output_dir, filename, expected_checksum)

print("All models downloaded to their respective directories successfully!")
