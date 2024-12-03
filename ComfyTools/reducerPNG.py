import os
import subprocess
import sys

from PIL import Image


def reduce_png_size(input_path, quality=85, width=None, height=None):
    """
    Reduce the size of a PNG image by resizing and compressing it using pngquant.

    Args:
        input_path (str): The path to the input PNG image.
        quality (int): The quality level for the saved image (default is 85).
        width (int, optional): The width to resize the image to. Preserves aspect ratio.
        height (int, optional): The height to resize the image to. Preserves aspect ratio.
    """
    # Define the output path with the quality percentage in the filename
    output_path = input_path.replace(".png", "{quality}.png")

    try:
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
                    "{quality}-{quality}",
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

        print(f"Reduced size image saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_image_path>")
        sys.exit(1)

    input_image_path = sys.argv[1]
    reduce_png_size(input_image_path, quality=85, width=1024)
