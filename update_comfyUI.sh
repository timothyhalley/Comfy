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


# Update all requirements manually
cd ~/Projects/Comfy/ComfyUI
pip3 install --upgrade -r requirements.txt

# make sure latest pyTorch
pip3 install --upgrade --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu

# install and update huggingface hub library for downloads
pip install --upgrade huggingface_hub

pip list
