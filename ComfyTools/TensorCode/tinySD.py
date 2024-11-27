"""
This module generates an image using the Pillow library.
"""

import torch
from diffusers import StableDiffusionPipeline
from PIL import Image

# Check if MPS is available and use it if possible
device = "mps" if torch.backends.mps.is_available() else "cpu"

# Load the pre-trained model
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4").to(
    device
)

# Define the prompt for the AI model
prompt = "A highly detailed and realistic scene of an egg on the surface of the moon. The egg is cracking open, and a tiny Godzilla is hatching out of it. The Earth is prominently visible in the background of the moon's surface as in a blue marble, and the scene is set under a clear, starry sky."


# Generate the image using the prompt
image = pipe(prompt, num_inference_steps=150, guidance_scale=10.0).images[0]

# Save the image to a file
image.save("tinySD.png")

print("Image generated and saved as tinySD.png")
