"""
This module is for downloading data from Hugging Face.
"""

import hashlib
import os

from huggingface_hub import hf_hub_download, login

base_path = "/Volumes/MySSD/ComfyUI"


# List of model URLs and their corresponding directories
models = {
    "v2-1_768-ema-pruned": {
        "url": "stabilityai/stable-diffusion-2-1",
        "dir": f"{base_path}/models/checkpoints/",
        "revision": "main",
        "filename": "v2-1_768-ema-pruned.safetensors",
        "checksum": "dcd690123cfc64383981a31d955694f6acf2072a80537fdb612c8e58ec87a8ac",
    },
    "ComfyOrg Flux1 FP8": {
        "url": "Comfy-Org/flux1-dev",
        "dir": f"{base_path}/models/controlnet/",
        "revision": "main",
        "filename": "flux1-dev-fp8.safetensors",
        "checksum": "8e91b68084b53a7fc44ed2a3756d821e355ac1a7b6fe29be760c1db532f3d88a",
    },
    "4x-ClearRealityV1": {
        "url": "skbhadra/ClearRealityV1",
        "dir": f"{base_path}/models/upscale_models",
        "revision": "main",
        "filename": "4x-ClearRealityV1.pth",
        "checksum": "a4cd3a25b00e0be949d4302fc774eb4d7f2ed5f47cdb51551e2d75fa6562e51e",
    },
    "v2_lora_ZoomIn2": {
        "url": "camenduru/AnimateDiff",
        "dir": f"{base_path}/models/AnimateDiff",
        "revision": "main",
        "filename": "v2_lora_ZoomIn.ckpt",
        "checksum": "70ce8b9057b173b9249c48aca5d66c8aa1d8aaa040fda394e50e37f3e278195e",
    },
    # CheckPoint Folder:
    "Juggernaut XLv6": {
        "url": "RunDiffusion/Juggernaut-XL-v6",
        "dir": f"{base_path}/models/checkpoints/",
        "revision": "main",
        "filename": "juggernautXL_version6Rundiffusion.safetensors",
        "checksum": "1fe6c7ec54c786040cdabc7b4e89720069d97096922e20d01f13e7764412b47f",
    },
    "Juggernaut XLv8": {
        "url": "RunDiffusion/Juggernaut-XL-v8",
        "dir": f"{base_path}/models/checkpoints/",
        "revision": "main",
        "filename": "juggernautXL_v8Rundiffusion.safetensors",
        "checksum": "aeb7e9e6897a1e58b10494bd989d001e3d4bc9b634633cd7b559838f612c2867",
    },
    "Think XL": {
        "url": "ThinkDiffusion/ThinkDiffusionXL",
        "dir": f"{base_path}/models/checkpoints/",
        "revision": "",
        "filename": "ThinkDiffusionXL.safetensors",
        "checksum": "a21c9949efcb8a0218f575aaff3fd5e8fedc508ca6757ddb44c5958cb0859f77",
    },
    "Anime Art": {
        "url": "nolual/majic",
        "dir": f"{base_path}/models/checkpoints/",
        "revision": "",
        "filename": "animeArtDiffusionXL_alpha3.safetensors",
        "checksum": "53bb4fdc63b36014201f2789eab73f3b2b3569a2a9a57b3efb28d4f17283e4c4",
    },
    "SD3.5 Large": {
        "url": "stabilityai/stable-diffusion-3.5-large",
        "dir": f"{base_path}/models/checkpoints/",
        "revision": "",
        "filename": "sd3.5_large.safetensors",
        "checksum": "ffef7a279d9134626e6ce0d494fba84fc1c7e720b3c7df2d19a09dc3796d8f93",
    },
    "SD3.5 Turbo": {
        "url": "stabilityai/stable-diffusion-3.5-large-turbo",
        "dir": f"{base_path}/models/checkpoints/",
        "revision": "",
        "filename": "sd3.5_large_turbo.safetensors",
        "checksum": "fb64610bf8d73eb064b8d528eef85d062bf2b4b1204ff7bc73e57ad28b24489c",
    },
    "SD3.5 Med": {
        "url": "stabilityai/stable-diffusion-3.5-medium",
        "dir": f"{base_path}/models/checkpoints/",
        "revision": "",
        "filename": "sd3.5_medium.safetensors",
        "checksum": "11fe06e22364b823dfeedc275912336b932b32a293a0b2f35ffac071990cc4de",
    },
    "SD XL Refiner": {
        "url": "stabilityai/stable-diffusion-xl-refiner-1.0",
        "dir": f"{base_path}/models/checkpoints/",
        "revision": "",
        "filename": "sd_xl_refiner_1.0_0.9vae.safetensors",
        "checksum": "8d0ce6c016004cbdacd50f937dad381d8c396628d621a7f97191470532780164",
    },
    "Epic Realism": {
        "url": "Justin-Choo/epiCRealism-Natural_Sin_RC1_VAE",
        "dir": f"{base_path}/models/checkpoints/",
        "revision": "",
        "filename": "epicrealism_naturalSinRC1VAE.safetensors",
        "checksum": "84d76a0328ee5a1a2a1d466ba7478ab59183e3fea385441528aa4c5d567fd43e",
    },
    "Photon AI": {
        "url": "WALIDALI/lcmphoton",
        "dir": f"{base_path}/models/checkpoints/",
        "revision": "",
        "filename": "photonLCM_v10.safetensors",
        "checksum": "f2d45bbd0f7d28b7ff5e33cf5f7dca82ccf7a14fa55a867ec4dc7f701cb2859f",
    },
    "Clay Cinematic": {
        "url": "artificialguybr/CinematicRedmond-SDXL",
        "dir": f"{base_path}/models/checkpoints/",
        "revision": "",
        "filename": "CinematicRedmond.safetensors",
        "checksum": "40b693cfe5831e8097290bb56ee93d7b2ecc644010b1dc78f803cbdbddb6f87e",
    },
    # Text Encoder / Clip Models
    "SD3.5 Diff - G": {
        "url": "stabilityai/stable-diffusion-3-medium",
        "dir": f"{base_path}/models/clip/",
        "revision": "text_encoders",
        "filename": "clip_g.safetensors",
        "checksum": "ec310df2af79c318e24d20511b601a591ca8cd4f1fce1d8dff822a356bcdb1f4",
    },
    "SD3.5 Diff - L": {
        "url": "stabilityai/stable-diffusion-3-medium",
        "dir": f"{base_path}/models/clip/",
        "revision": "text_encoders",
        "filename": "clip_l.safetensors",
        "checksum": "660c6f5b1abae9dc498ac2d21e1347d2abdb0cf6c0c0c8576cd796491d9a6cdd",
    },
    "Mochi FP16": {
        "url": "Comfy-Org/mochi_preview_repackaged",
        "dir": f"{base_path}/models/text_encoders/",
        "revision": "split_files/text_encoders",
        "filename": "t5xxl_fp16.safetensors",
        "checksum": "6e480b09fae049a72d2a8c5fbccb8d3e92febeb233bbe9dfe7256958a9167635",
    },
    "SDXL VAE": {
        "url": "stabilityai/sdxl-vae",
        "dir": f"{base_path}/models/vae/",
        "revision": "",
        "filename": "sdxl_vae.safetensors",
        "checksum": "63aeecb90ff7bc1c115395962d3e803571385b61938377bc7089b36e81e92e2e",
    },
    "FLUX 1 DEV": {
        "url": "black-forest-labs/FLUX.1-dev",
        "dir": f"{base_path}/models/checkpoints/",
        "revision": "",
        "filename": "flux1-dev.safetensors",
        "checksum": "4610115bb0c89560703c892c59ac2742fa821e60ef5871b33493ba544683abd7",
    },
    # ControlNet Models
    "Canny SDXL": {
        "url": "diffusers/controlnet-canny-sdxl-1.0",
        "dir": f"{base_path}/models/controlnet",
        "revision": "main",
        "filename": "diffusion_pytorch_model.fp16.safetensors",
        "checksum": "b2e7d3921058a442cc80430d1ec8847f42599c705e2451c95e77cf4dcf8d6c25",
    },
    "FLUX Diff": {
        "url": "Shakker-Labs/FLUX.1-dev-ControlNet-Union-Pro",
        "dir": f"{base_path}/models/controlnet",
        "revision": "",
        "filename": "diffusion_pytorch_model.safetensors",
        "checksum": "981a01d6a9575e90820275eda61b33d4ecab0928c68a4f31b132b9687930f90a",
    },
    "FLUX Canny": {
        "url": "XLabs-AI/flux-controlnet-collections",
        "dir": f"{base_path}/models/controlnet",
        "revision": "",
        "filename": "flux-canny-controlnet-v3.safetensors",
        "checksum": "6546f29049796101a6370db0a43d2671d0294287c36b2b4e8792cf9e68f0eaf0",
    },
    "FLUX Depth": {
        "url": "XLabs-AI/flux-controlnet-collections",
        "dir": f"{base_path}/models/controlnet",
        "revision": "",
        "filename": "flux-depth-controlnet-v3.safetensors",
        "checksum": "d52eeaf8072de89d72b1ee79e3bdc79b5d795ed0a6881a029bbe13d833df7e5f",
    },
    "FLUX V3": {
        "url": "XLabs-AI/flux-controlnet-collections",
        "dir": f"{base_path}/models/controlnet",
        "revision": "",
        "filename": "flux-hed-controlnet-v3.safetensors",
        "checksum": "31c110ae4557c19f1c2d74f824c20ea4c340161106df25cf7caf298e2f22f441",
    },
    "SD15 Monster": {
        "url": "monster-labs/control_v1p_sd15_qrcode_monster",
        "dir": f"{base_path}/models/controlnet",
        "revision": "v2",
        "filename": "control_v1p_sd15_qrcode_monster_v2.safetensors",
        "checksum": "fc985da5850a03033c9e28032532f406ae04bd127178ae5bc6d3ec0502b25253",
    },
    # VAE
    "SDXL-VAE Diff": {
        "url": "stabilityai/sdxl-vae",
        "dir": f"{base_path}/models/vae",
        "revision": "main",
        "filename": "diffusion_pytorch_model.safetensors",
        "checksum": "1598f3d24932bcfe6634e8b618ea1e30ab1d57f5aad13a6d2de446d2199f2341",
    },
    "Mochi": {
        "url": "Comfy-Org/mochi_preview_repackaged",
        "dir": f"{base_path}/models/vae",
        "revision": "split_files/vae",
        "filename": "mochi_vae.safetensors",
        "checksum": "1be451cec94b911980406169286babc5269e7cf6a94bbbbdf45e8d3f2c961083",
    },
    "FLUX Schnell": {
        "url": "black-forest-labs/FLUX.1-schnell",
        "dir": f"{base_path}/models/vae",
        "revision": "",
        "filename": "ae.safetensors",
        "checksum": "afc8e28272cd15db3919bacdb6918ce9c1ed22e96cb12c4d5ed0fba823529e38",
    },
    "SD MAE": {
        "url": "stabilityai/sd-vae-ft-mse-original",
        "dir": f"{base_path}/models/vae",
        "revision": "",
        "filename": "vae-ft-mse-840000-ema-pruned.safetensors",
        "checksum": "735e4c3a447a3255760d7f86845f09f937809baa529c17370d83e4c3758f3c75",
    },
    # Lora Models
    "FluxRealismLora": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": f"{base_path}/models/loras",
        "revision": "",
        "filename": "realism_lora.safetensors",
        "checksum": "0a83a924b822b70b5e458d27935ebfa7713edaee04ff9f194209525354031eca",
    },
    "Flux Scenery": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": f"{base_path}/models/loras",
        "revision": "",
        "filename": "scenery_lora.safetensors",
        "checksum": "1956be0c699aaa7f806c35d0e4e9aa94b72d54f9c841a4fc40b876692e4ed756",
    },
    "Lego Brickheadz": {
        "url": "nerijs/lego-brickheadz-xl",
        "dir": f"{base_path}/models/loras/",
        "revision": "",
        "filename": "legobrickheadz-v1.0-000004.safetensors",
        "checksum": "723b7fc7e7c599f0f6f8252ce12cde266fbc078fe316e262d2d5955903389d13",
    },
    "FLUX Realism": {
        "url": "XLabs-AI/flux-RealismLora",
        "dir": f"{base_path}/models/loras",
        "revision": "",
        "filename": "lora.safetensors",
        "checksum": "0a83a924b822b70b5e458d27935ebfa7713edaee04ff9f194209525354031eca",
    },
    "FLUX Anime": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": f"{base_path}/models/loras",
        "revision": "",
        "filename": "anime_lora.safetensors",
        "checksum": "a079252bee7c27113478c276b8155873933961d5cfaec8f56b877bc759b08865",
    },
    "FLUX LoRAs Real": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": f"{base_path}/models/loras",
        "revision": "",
        "filename": "realism_lora.safetensors",
        "checksum": "0a83a924b822b70b5e458d27935ebfa7713edaee04ff9f194209525354031eca",
    },
    "FLUX Disney": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": f"{base_path}/models/loras",
        "revision": "",
        "filename": "disney_lora.safetensors",
        "checksum": "e37353b1242f9cfe11bd52528f235b9a1028855aad25cd3d4d593f4410cb7207",
    },
    "FLUX LoRAs Scenery": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": f"{base_path}/models/loras",
        "revision": "",
        "filename": "scenery_lora.safetensors",
        "checksum": "1956be0c699aaa7f806c35d0e4e9aa94b72d54f9c841a4fc40b876692e4ed756",
    },
    "FLUX MJV6": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": f"{base_path}/models/loras",
        "revision": "",
        "filename": "mjv6_lora.safetensors",
        "checksum": "0643a893142c77c889bac2646796181563f02cdcdb0d066e322c1ffb7ba758f8",
    },
    "FLUX Furry": {
        "url": "XLabs-AI/flux-lora-collection",
        "dir": f"{base_path}/models/loras",
        "revision": "",
        "filename": "furry_lora.safetensors",
        "checksum": "b53633e75dc91882d9da57dbb3416b3767c940cdb3227bf341dd54ffbb51d152",
    },
    "Alien God SDXL": {
        "url": "CiroN2022/alien-god",
        "dir": f"{base_path}/models/loras",
        "revision": "",
        "filename": "Alien_God_sdxl.safetensors",
        "checksum": "e8407cfd38c94cbed4e2ecd0c6f0e0db67ee9ea3c1a6dd3bc53ae79ca801c884",
    },
    "CLAYMATE_V2.03": {
        "url": "AI2lab/SDXL-loras",
        "dir": f"{base_path}/models/loras",
        "revision": "main",
        "filename": "CLAYMATE_V2.03_.safetensors",
        "checksum": "fc1790ddec807108bb4125748c37b5b33c23806f2b5f74d1c5b8b19bf68b2284",
    },
    "Clay-XL-v2": {
        "url": "AI2lab/SDXL-loras",
        "dir": f"{base_path}/models/loras",
        "revision": "main",
        "filename": "DD-made-of-clay-XL-v2.safetensors",
        "checksum": "cdc4c3e276b857b21b9c6308f426baa446027bb734b5bbdeecaa2a06d9a4f41a",
    },
    "BigEye 1": {
        "url": "2vXpSwA7/iroiro-lora",
        "dir": f"{base_path}/models/loras",
        "revision": "main",
        "filename": "sdxl/sdxl-eye_bigeye.safetensors",
        "checksum": "f60c5f29a44c548a18908035c747bee17c6816c5a49eeca8d9dddadbc7bad636",
    },
    "Monster SD V2": {
        "url": "AI2lab/SDXL-loras",
        "dir": f"{base_path}/models/loras",
        "revision": "main",
        "filename": "PE_PencilDrawing.safetensors",
        "checksum": "002ec698232dc1cb50b27e7b56b32f397e6528e07b0bcb4ab8a421c866c1e7bc",
    },
    "xinsir SDXL": {
        "url": "AI2lab/SDXL-loras",
        "dir": f"{base_path}/models/loras",
        "revision": "main",
        "filename": "DD-made-of-clay-XL-v2.safetensors",
        "checksum": "cdc4c3e276b857b21b9c6308f426baa446027bb734b5bbdeecaa2a06d9a4f41a",
    },
    # Diffusion Models
    "Mochi Model": {
        "url": "Comfy-Org/mochi_preview_repackaged",
        "dir": f"{base_path}/models/diffusion_models",
        "revision": "split_files/diffusion_models",
        "filename": "mochi_preview_bf16.safetensors",
        "checksum": "e445b9b393c70c431543b062cc16ee29b5dc4dc187487fa3e1f5a4b6162c8be1",
    },
    "GGUF Unet Q6_K": {
        "url": "city96/FLUX.1-schnell-gguf",
        "dir": f"{base_path}/models/diffusion_models",
        "filename": "flux1-schnell-Q6_K.gguf",
        "revision": "",
        "checksum": "a42fd143cec4d7194da281dc8d23a8fe54b16875a13423c042cb545d1da6fa50",
    },
    # IP Adaptor
    "FLUX IP": {
        "url": "XLabs-AI/flux-ip-adapter-v2",
        "dir": f"{base_path}/models/ipadapter",
        "revision": "",
        "filename": "ip_adapter.safetensors",
        "checksum": "8f2bfddaffc4fe2a6667bef24c8ce6075e81d01d0f6b0f9adbe46ad686057ee2",
    },
    "FLUX Adapter": {
        "url": "openai/clip-vit-large-patch14",
        "dir": f"{base_path}/models/clip",
        "revision": "",
        "filename": "model.safetensors",
        "checksum": "a2bf730a0c7debf160f7a6b50b3aaf3703e7e88ac73de7a314903141db026dcb",
    },
    # Clip Vision Model(s)
    "Clip Vision H": {
        "url": "lllyasviel/misc",
        "dir": f"{base_path}/models/clip",
        "revision": "main",
        "filename": "clip_vision_vit_h.safetensors",
        "checksum": "a2bf730a0c7debf160f7a6b50b3aaf3703e7e88ac73de7a314903141db026dcb",
    },
    # "Clip Vision by comfyanonymous": {
    #     "url": "comfyanonymous/clip_vision_g",
    #     "dir": f"{base_path}/models/clip_vision",
    #     "revision": "",
    #     "filename": "clip_vision_g.safetensors",
    #     "checksum": "9908329b3ead722a693ea400fab1d7c9ec91d6736fd194a94d20d793457f9c2e",
    # },
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
def download_and_verify(
    model_name, model_url, output_dir, revision_sub, filename, expected_checksum
):
    file_path = os.path.join(output_dir, filename)
    if os.path.exists(file_path):
        # Calculate the checksum of the existing file
        current_checksum = calculate_checksum(file_path)
        if current_checksum == expected_checksum:
            print(f"{model_name}\t{model_url}:{filename}\t👍")
            return
        else:
            print(
                f"\n{model_name}\t{model_url}:{filename} exists but checksum is incorrect.\t👎\n"
            )
            return
    else:
        print(
            f"\n{model_name}\t{model_url}:{filename} does not exist. Downloading...\t🌎\n"
        )

    # Download the file
    hf_hub_download(
        repo_id=model_url,
        revision=revision_sub,
        filename=filename,
        local_dir=output_dir,
    )
    print(f"Downloaded {model_url} -- {filename} to {file_path}")


# Download each model into its specified directory
for model_name, model_info in models.items():
    model_url = model_info["url"]
    output_dir = model_info["dir"]
    revision_sub = model_info["revision"]
    filename = model_info["filename"]
    expected_checksum = model_info["checksum"]
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
    download_and_verify(
        model_name, model_url, output_dir, revision_sub, filename, expected_checksum
    )

print("All models downloaded to their respective directories successfully!")
