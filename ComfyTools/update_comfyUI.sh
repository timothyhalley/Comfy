#!/bin/zsh


#### --- Modified to only update ENV since using desktop version --- ####


# check python version
# install verson via:
#   pyenv install --list
#   pyenv install 3.12.7
#   pyenv global 3.12.7
#   source new shell!!!
# Also modify shell start:
#   Ensure your shell configuration file (e.g., .zshrc, .bashrc) includes the pyenv initialization. Add these lines if they are missing:
#   export PATH="$HOME/.pyenv/bin:$PATH"
#   eval "$(pyenv init --path)"
#   eval "$(pyenv init -)"
#   eval "$(pyenv virtualenv-init -)"

pyenv global
export PYTORCH_ENABLE_MPS_FALLBACK=1

# Install comfyUI from git repo
# cd ~/Projects/Comfy
# git clone https://github.com/comfyanonymous/ComfyUI.git
# cd ComfyUI
# rd .git

# install custom node manager

#   download manager via:
# cd custom_nodes
# git clone https://github.com/ltdrdata/ComfyUI-Manager.git

# Other nodes
#git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus.git
# git clone https://github.com/XLabs-AI/x-flux-comfyui.git
# git clone https://github.com/city96/ComfyUI-GGUF.git

# git clone https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes.git
# git clone https://github.com/twri/sdxl_prompt_styler.git
# git clone https://github.com/TripleHeadedMonkey/ComfyUI_MileHighStyler

# `git clone https://github.com/BlenderNeko/ComfyUI_Noise`


##
# git clone https://github.com/smthemex/ComfyUI_StoryDiffusion.git
# cd ~/Projects/Comfy/ComfyUI/custom_nodes/ComfyUI_StoryDiffusion
# pip3 install --upgrade -r requirements.txt
# cd ~/Projects/Comfy/ComfyUI/custom_nodes
# git clone https://github.com/pythongosssss/ComfyUI-WD14-Tagger.git

# Image Tagger 
# cd ~/Projects/Comfy/ComfyUI/custom_nodes/ComfyUI-WD14-Tagger
# pip3 install --upgrade -r requirements.txt
# cd ~/Projects/Comfy/ComfyUI/custom_nodes

# Manager Nodes
# git clone https://github.com/crystian/ComfyUI-Crystools.git
# cd ~/Projects/Comfy/ComfyUI/custom_nodes/ComfyUI-Crystools
# pip3 install --upgrade -r requirements.txt

# Update all requirements manually
cd ~/Projects/Comfy/ComfyUI
pip3 install --upgrade -r requirements.txt
pip3 install --upgrade gguf

# Additional requirements
pip3 install --upgrade deepdiff

# make sure latest pyTorch
pip3 install --upgrade --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu

# install and update huggingface hub library for downloads
pip3 install --upgrade huggingface_hub

pip3 list

# Modify the YAML file to locate single model directory
# Define the directory and file path
# dir_path="."
# file_path="$dir_path/extra_model_paths.yaml"

# # Create the directory if it doesn't exist
# mkdir -p $dir_path

# # Create and write content to the file
# echo "FILE CFG: $file_path"
# cat <<EOL > $file_path
# comfyui:
#     BASE_PATH: /Volumes/MySSD/ComfyUI/
#     # You can use is_default to mark that these folders should be listed first, and used as the default dirs for eg downloads
#     #is_default: true
#     checkpoints: /Volumes/MySSD/ComfyUI//Volumes/MySSD/ComfyUI/models/checkpoints/
#     clip: /Volumes/MySSD/ComfyUI//Volumes/MySSD/ComfyUI/models/clip/
#     clip_vision: /Volumes/MySSD/ComfyUI//Volumes/MySSD/ComfyUI/models/clip_vision/
#     configs: /Volumes/MySSD/ComfyUI//Volumes/MySSD/ComfyUI/models/configs/
#     controlnet: /Volumes/MySSD/ComfyUI//Volumes/MySSD/ComfyUI/models/controlnet/
#     diffusion_models: |cd C
#         /Volumes/MySSD/ComfyUI//Volumes/MySSD/ComfyUI/models/diffusion_models
#         /Volumes/MySSD/ComfyUI//Volumes/MySSD/ComfyUI/models/unet
#     embeddings: /Volumes/MySSD/ComfyUI//Volumes/MySSD/ComfyUI/models/embeddings/
#     loras: /Volumes/MySSD/ComfyUI//Volumes/MySSD/ComfyUI/models/loras/
#     upscale_models: /Volumes/MySSD/ComfyUI//Volumes/MySSD/ComfyUI/models/upscale_/Volumes/MySSD/ComfyUI//Volumes/MySSD/ComfyUI/models/
#     vae: /Volumes/MySSD/ComfyUI//Volumes/MySSD/ComfyUI/models/vae/
# EOL

# Inform the user
# cat $file_path

