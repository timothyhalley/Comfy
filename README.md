# ComfyUI
Comfy Scripts and Tools to use

# Sync model directory with SSD:
mkdir -p /Volumes/MySSD/Project/Comfy/ComfyUI/models
rsync -avP --include='*/' --include='*.safetensors' --include='*.GGUF' --exclude='*' [Source] [Destination]
rsync -avP --include='*/' --include='*.safetensors' --include='*.GGUF' --exclude='.cache/' --exclude='*' [Source] [Destination]

# Delete .cache directories in sub folders:
find /path/to/directory -type d -name ".cache" -exec rm -rf {} +


MBP: /Users/I850916/Projects/Comfy/ComfyUI//Volumes/MySSD/ComfyUI/models/
MAC Mini1: ~/Projects/Comfy/ComfyUI//Volumes/MySSD/ComfyUI/models/
SSD: /Volumes/MySSD/Project/Comfy/ComfyUI//Volumes/MySSD/ComfyUI/models/

# Useful links and info:
* Useful links for ComfyUI modeling

# SD Update Oct 22
https://blog.comfy.org/sd3-5-comfyui/


# AI Workflow Links:
https://openaijourney.com/best-comfyui-workflows/
https://github.com/comfyanonymous/ComfyUI_examples%  
https://civitai.com/models
https://comfyanonymous.github.io/ComfyUI_examples/ 
https://tensor.art/workflows


# Best Img2Img --> 
https://learn.thinkdiffusion.com/a-list-of-the-best-comfyui-workflows/#img2img-comfyui-workflow

# Best Img2Vid -->
https://comfyanonymous.github.io/ComfyUI_examples/mochi/
https://huggingface.co/genmo/mochi-1-preview



# Prompt for alien:

Imagine a grand, futuristic lab with sleek metallic walls that glimmer with the soft glow of ambient lighting. In the center of the room stands the quantum computer, a colossal structure that emanates a soft, pulsating light from its core. Its surface is made of a translucent material, allowing you to see the intricate web of quantum particles dancing inside.

The engineer, an evolved being with a size and strength that supports significantly more gravity, stands confidently next to the computer. Their form is still human-like, but with an aura of god-like presence. Their eyes reflect deep thought and profound wisdom, hinting at the vast knowledge they possess. The engineer's skin is iridescent, having adapted to the conditions of long-term sleep chambers, giving them an almost ethereal glow.

The engineer's advanced biomechanical suit enhances their capabilities, seamlessly integrating with their body. The suit allows them to interact with the quantum computer through holographic displays that respond to their every gesture. The atmosphere is charged with an aura of discovery, as the engineer prepares to unlock the secrets of the quantum computer. The room hums with the low-frequency sound of advanced machinery, creating a sense of anticipation and excitement.

The combination of their evolved form, deep intellect, and advanced technology creates a mesmerizing and awe-inspiring scene.

The image is highly detailed with natural textures and intricate patterns, showcasing realistic lighting and deep shadows to give the scene a sense of depth. The focus should be clearly defined, making every object appear sharply focused with pin-sharp details. There are no watermarks visable.