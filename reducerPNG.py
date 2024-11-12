import os
import subprocess

from PIL import Image


def reduce_png_size(input_path, output_path, quality=85, width=None, height=None):
    """
    Reduce the size of a PNG image by resizing and compressing it using pngquant.

    Args:
        input_path (str): The path to the input PNG image.
        output_path (str): The path to save the reduced size PNG image.
        quality (int): The quality level for the saved image (default is 85).
        width (int, optional): The width to resize the image to. Preserves aspect ratio.
        height (int, optional): The height to resize the image to. Preserves aspect ratio.
    """
    # Open an image file
    with Image.open(input_path) as img:
        # Resize the image if width and height are provided
        if width or height:
            img.thumbnail((width or img.width, height or img.height))

        # Save a temporary copy of the image
        temp_path = output_path.replace(".png", "_temp.png")
        img.save(temp_path, optimize=True)

        # Compress the image using pngquant
        subprocess.run(
            [
                "pngquant",
                "--quality",
                str(quality),
                "--output",
                output_path,
                "--force",
                temp_path,
            ],
            check=True,
        )

    # Clean up the temporary file
    if os.path.exists(temp_path):
        os.remove(temp_path)


INPUT_IMG_PATH = "./WorkflowImages/TwoBrothers.png"
OUTPUT_IMG_PATH = "./WorkflowImages/TwoBrothers_reduced.png"

# Reduce the PNG size by compressing and optionally resizing
reduce_png_size(INPUT_IMG_PATH, OUTPUT_IMG_PATH, quality=95, width=1024)
print(f"Reduced size image saved to {OUTPUT_IMG_PATH}")
