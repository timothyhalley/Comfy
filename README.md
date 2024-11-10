# Comfy
Comfy Scripts and Tools to use

# Sync model directory with SSD:
mkdir -p /Volumes/MySSD/Project/Comfy/ComfyUI/models
rsync -avP --include='*/' --include='*.safetensors' --include='*.GGUF' --exclude='*' [Source] [Destination]
rsync -avP --include='*/' --include='*.safetensors' --include='*.GGUF' --exclude='.cache/' --exclude='*' [Source] [Destination]

# Delete .cache directories in sub folders:
find /path/to/directory -type d -name ".cache" -exec rm -rf {} +


MBP: /Users/I850916/Projects/Comfy/ComfyUI/models/
MAC Mini1: ~/Projects/Comfy/ComfyUI/models/
SSD: /Volumes/MySSD/Project/Comfy/ComfyUI/models/

# Useful links and info:
* Useful links for ComfyUI modeling

# SD Update Oct 22
https://blog.comfy.org/sd3-5-comfyui/


# AI Workflow Links:
https://openaijourney.com/best-comfyui-workflows/
https://github.com/comfyanonymous/ComfyUI_examples%  
https://civitai.com/models


# Best Img2Img --> 
https://learn.thinkdiffusion.com/a-list-of-the-best-comfyui-workflows/#img2img-comfyui-workflow
