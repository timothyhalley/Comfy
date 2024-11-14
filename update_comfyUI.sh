#!/bin/zsh

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

# Install comfyUI from git repo
cd ~/Projects/Comfy
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
# rd .git

# install custom node manager

#   download manager via:
cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git

# Other nodes
git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus.git

# Manager Nodes
# Install / Add: ComfyUI Impact Pack

# Custom Node for CPU and Memory
# Open the ComfyUI Manager.
# Select the Custom Nodes Manager.
# Search for “crystools” and install it.
git clone https://github.com/crystian/ComfyUI-Crystools.git


# Update all requirements manually
cd ~/Projects/Comfy/ComfyUI
pip3 install --upgrade -r requirements.txt

# make sure latest pyTorch
pip3 install --upgrade --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu

# install and update huggingface hub library for downloads
pip3 install --upgrade huggingface_hub

pip3 list

# Modify the YAML file to locate single model directory
# Define the directory and file path
dir_path="."
file_path="$dir_path/extra_model_paths.yaml"

# Create the directory if it doesn't exist
mkdir -p $dir_path

# Create and write content to the file
echo "FILE CFG: $file_path"
cat <<EOL > $file_path
comfyui:
    base_path: /Volumes/MySSD/ComfyUI/
    # You can use is_default to mark that these folders should be listed first, and used as the default dirs for eg downloads
    #is_default: true
    checkpoints: models/checkpoints/
    clip: models/clip/
    clip_vision: models/clip_vision/
    configs: models/configs/
    controlnet: models/controlnet/
    diffusion_models: |
        models/diffusion_models
        models/unet
    embeddings: models/embeddings/
    loras: models/loras/
    upscale_models: models/upscale_models/
    vae: models/vae/
EOL

# Inform the user
cat $file_path

