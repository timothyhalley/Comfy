import torch
from diffusers import FluxPipeline

# Ensure CPU is selected
device = torch.device("cpu")
print("CPU device selected")

# Load the pipeline and move it to the appropriate device
pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-schnell", torch_dtype=torch.float32
).to(device)
pipe.enable_model_cpu_offload()
pipe.vae.enable_slicing()
pipe.vae.enable_tiling()

PROMPT = "a tiny astronaut hatching from an egg on the moon"

# Generate the image with the specified device
with torch.no_grad():
    out = pipe(
        prompt=PROMPT,
        guidance_scale=0.0,
        height=256,  # Reduced height
        width=256,  # Reduced width
        num_inference_steps=4,
        max_sequence_length=256,
    ).images[0]
    out.save("astroEgg.png")


# import gc
# import os

# import torch
# from diffusers import FluxPipeline

# # Set the high watermark ratio
# os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"

# # Check if MPS is available
# if torch.backends.mps.is_available():
#     device = torch.device("mps")
#     print("MPS device selected")
#     gc.collect()
#     print("Garbage collected and purged!")
#     torch.mps.set_per_process_memory_fraction(0.5)
#     print("MPS memory set to 50%...")
# else:
#     device = torch.device("cpu")
#     print("CPU device selected")

# pipe = FluxPipeline.from_pretrained(
#     "black-forest-labs/FLUX.1-schnell", torch_dtype=torch.bfloat16
# ).to(device)
# pipe.enable_sequential_cpu_offload()
# pipe.vae.enable_slicing()
# pipe.vae.enable_tiling()

# # casting here instead of in the pipeline constructor because doing so in the constructor loads all models into CPU memory at once
# pipe.to(torch.float16)

# PROMPT = "a tiny astronaut hatching from an egg on the moon"

# out = pipe(
#     prompt=PROMPT,
#     guidance_scale=0.0,
#     height=128,  # Further reduced height for testing
#     width=128,  # Further reduced width for testing
#     num_inference_steps=4,
#     max_sequence_length=256,
# ).images[0]
# out.save("astroEgg.png")
