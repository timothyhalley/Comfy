import argparse
import os
import sys

from PIL import Image


def reduce_image_size(input_path, quality=85, width=None, height=None):
    """
    Reduce the size of an image (PNG or JPEG) by resizing and compressing it.

    Args:
        input_path (str): The path to the input image (PNG or JPEG).
        quality (int): The quality level for the saved image (1-100, higher means better quality and larger size).
        width (int, optional): The width to resize the image to. Preserves aspect ratio.
        height (int, optional): The height to resize the image to. Preserves aspect ratio.
    """
    # Define the output path with the quality percentage in the filename
    base_name, ext = os.path.splitext(input_path)
    output_path = f"{base_name}_{quality}.jpeg"

    try:
        # Open an image file
        with Image.open(input_path) as img:
            # Resize the image if width and height are provided
            if width or height:
                img.thumbnail((width or img.width, height or img.height))

            # Convert the image to RGB mode if necessary for JPEG format
            if img.mode in ("RGBA", "LA") or (
                img.mode == "P" and "transparency" in img.info
            ):
                img = img.convert("RGB")

            # Save the image with the specified quality
            img.save(output_path, "JPEG", quality=quality, optimize=True)

        print(f"Reduced size image saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Reduce the size of an image (PNG or JPEG)."
    )
    parser.add_argument(
        "input_image_path", type=str, help="The path to the input image."
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=85,
        help="The quality level for the saved image (1-100).",
    )
    parser.add_argument(
        "--width",
        type=int,
        help="The width to resize the image to. Preserves aspect ratio.",
    )
    parser.add_argument(
        "--height",
        type=int,
        help="The height to resize the image to. Preserves aspect ratio.",
    )

    args = parser.parse_args()
    reduce_image_size(
        args.input_image_path,
        quality=args.quality,
        width=args.width,
        height=args.height,
    )
