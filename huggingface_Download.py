import os

from huggingface_hub import hf_hub_download, login

# List of model URLs and their corresponding directories
models = {
    "Anime Art Diffusion XL Alpha": {
        "url": "nolual/majic",
        "dir": "./ComfyUI/models/checkpoints/",
        "filename": "animeArtDiffusionXL_alpha3.safetensors",
    },
    "SD3.5 Large": {
        "url": "stabilityai/stable-diffusion-3.5-large",
        "dir": "./ComfyUI/models/checkpoints/",
        "filename": "sd3.5_large.safetensors",
    },
    "SD3.5 Turbo": {
        "url": "stabilityai/stable-diffusion-3.5-large-turbo",
        "dir": "./ComfyUI/models/checkpoints/",
        "filename": "sd3.5_large_turbo.safetensors",
    },
    "SD3.5 Medium": {
        "url": "stabilityai/stable-diffusion-3.5-medium",
        "dir": "./ComfyUI/models/checkpoints/",
        "filename": "sd3.5_medium.safetensors",
    },
    "SD3.5 Diffusion Text Encoder - G": {
        "url": "stabilityai/stable-diffusion-3-medium",
        "dir": "./ComfyUI/models/clip/",
        "filename": "text_encoders/clip_g.safetensors",
    },
    "SD3.5 Diffusion Text Encoder - L": {
        "url": "stabilityai/stable-diffusion-3-medium",
        "dir": "./ComfyUI/models/clip/",
        "filename": "text_encoders/clip_l.safetensors",
    },
    "SD3.5 Diffusion Text Encoder - FP16": {
        "url": "stabilityai/stable-diffusion-3-medium",
        "dir": "./ComfyUI/models/clip/",
        "filename": "text_encoders/t5xxl_fp16.safetensors",
    },
    "SD XL Refiner 1.0": {
        "url": "stabilityai/stable-diffusion-xl-refiner-1.0",
        "dir": "./ComfyUI/models/checkpoints/",
        "filename": "sd_xl_refiner_1.0_0.9vae.safetensors",
    },
    "SDXL VAE": {
        "url": "stabilityai/sdxl-vae",
        "dir": "./ComfyUI/models/vae/",
        "filename": "sdxl_vae.safetensors",
    },
    "FLUX 1 DEV": {
        "url": "black-forest-labs/FLUX.1-dev",
        "dir": "./ComfyUI/models/unet/",
        "filename": "flux1-dev.safetensors",
    },
    # XLabs-AI/flux-controlnet-collections
    "FLUX ControlNet Diff": {
        "url": "Shakker-Labs/FLUX.1-dev-ControlNet-Union-Pro",
        "dir": "./ComfyUI/models/controlnet",
        "filename": "diffusion_pytorch_model.safetensors",
    },
    "FLUX ControlNet Canny": {
        "url": "XLabs-AI/flux-controlnet-collections",
        "dir": "./ComfyUI/models/controlnet",
        "filename": "flux-canny-controlnet-v3.safetensors",
    },
    "FLUX ControlNet Depth": {
        "url": "XLabs-AI/flux-controlnet-collections",
        "dir": "./ComfyUI/models/controlnet",
        "filename": "flux-depth-controlnet-v3.safetensors",
    },
    "FLUX ControlNet V3": {
        "url": "XLabs-AI/flux-controlnet-collections",
        "dir": "./ComfyUI/models/controlnet",
        "filename": "flux-hed-controlnet-v3.safetensors",
    },
    "SD15 Monster Control": {
        "url": "monster-labs/control_v1p_sd15_qrcode_monster",
        "dir": "./ComfyUI/models/controlnet",
        "filename": "v2/control_v1p_sd15_qrcode_monster_v2.safetensors",
    },
    # VAE
    "FLUX VAE": {
        "url": "black-forest-labs/FLUX.1-schnell",
        "dir": "./ComfyUI/models/vae",
        "filename": "ae.safetensors",
    },
    "FLUX VAE Schnell": {
        "url": "black-forest-labs/FLUX.1-schnell",
        "dir": "./ComfyUI/models/vae",
        "filename": "flux1-schnell.safetensors",
    },
    # Lora Models
    "XL Lego Brickheadz": {
        "url": "nerijs/lego-brickheadz-xl",
        "dir": "./ComfyUI/models/loras/",
        "filename": "legobrickheadz-v1.0-000004.safetensors",
    },
    "LEGO Minifig XL": {
        "url": "nerijs/lego-minifig-xl",
        "dir": "./ComfyUI/models/loras/",
        "filename": "legominifig-v1.0-000003.safetensors",
    },
    "FLUX LoRAs Base": {
        "url": "XLabs-AI/flux-RealismLora",
        "dir": "./ComfyUI/models/loras",
        "filename": "lora.safetensors",
    },
    "FLUX LoRAs Anime": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": "./ComfyUI/models/loras",
        "filename": "anime_lora.safetensors",
    },
    "FLUX LoRAs Real": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": "./ComfyUI/models/loras",
        "filename": "realism_lora.safetensors",
    },
    "FLUX LoRAs Disney": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": "./ComfyUI/models/loras",
        "filename": "disney_lora.safetensors",
    },
    "FLUX LoRAs Scenery": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": "./ComfyUI/models/loras",
        "filename": "scenery_lora.safetensors",
    },
    "FLUX LoRAs MJV6": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": "./ComfyUI/models/loras",
        "filename": "mjv6_lora.safetensors",
    },
    "FLUX LoRAs Furry": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": "./ComfyUI/models/loras",
        "filename": "furry_lora.safetensors",
    },
    "Alien God SDXL": {
        "url": "CiroN2022/alien-god",
        "dir": "./ComfyUI/models/loras",
        "filename": "Alien_God_sdxl.safetensors",
    },
    # GGUF Models for FLUX
    "GGUF Unet Q6_K": {
        "url": "city96/FLUX.1-schnell-gguf",
        "dir": "./ComfyUI/models/diffusion_models/FLUX1",
        "filename": "flux1-schnell-Q6_K.gguf",
    },
    "GGUF Unet F16": {
        "url": "city96/FLUX.1-dev-gguf",
        "dir": "./ComfyUI/models/diffusion_models/FLUX1",
        "filename": "flux1-dev-F16.gguf",
    },
    "GGUF Unet Q80": {
        "url": "city96/FLUX.1-dev-gguf",
        "dir": "./ComfyUI/models/diffusion_models/FLUX1",
        "filename": "flux1-dev-Q8_0.gguf",
    },
    "GGUF Encoder Q8_0": {
        "url": "city96/t5-v1_1-xxl-encoder-gguf",
        "dir": "./ComfyUI/models/clip",
        "filename": "t5-v1_1-xxl-encoder-Q8_0.gguf",
    },
    # IP Adaptor
    "FLUX IP Adapter": {
        "url": "XLabs-AI/flux-ip-adapter-v2",
        "dir": "./ComfyUI/models/ipadapter",
        "filename": "ip_adapter.safetensors",
    },
    "FLUX Clip Adapter": {
        "url": "openai/clip-vit-large-patch14",
        "dir": "./ComfyUI/models/clip",
        "filename": "model.safetensors",
    },
}

# Log in to Hugging Face
login()

# Download each model into its specified directory
for model_name, model_info in models.items():
    model_url = model_info["url"]
    output_dir = model_info["dir"]
    filename = model_info["filename"]
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
    file_path = os.path.join(output_dir, filename)
    hf_hub_download(repo_id=model_url, filename=filename, local_dir=output_dir)
    print(f"Downloaded {model_name} to {file_path}")

print("All models downloaded to their respective directories successfully!")
