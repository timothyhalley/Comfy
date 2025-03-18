import argparse
import os

from PIL import Image


def reduce_image_size_in_folder(folder_path, quality=85, width=None, height=None):
    """
    Reduce the size of all PNG or JPEG images in a folder by resizing and compressing them.

    Args:
        folder_path (str): The path to the folder containing the images.
        quality (int): The quality level for the saved images (1-100, higher means better quality and larger size).
        width (int, optional): The width to resize the images to. Preserves aspect ratio.
        height (int, optional): The height to resize the images to. Preserves aspect ratio.
    """
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        input_path = os.path.join(folder_path, file_name)

        # Process only PNG or JPEG files
        if os.path.isfile(input_path) and file_name.lower().endswith(
            (".png", ".jpg", ".jpeg")
        ):
            # Extract the directory and base name of the file
            base_name, ext = os.path.splitext(file_name)

            # Define the output file name with the quality number prepended
            output_file_name = f"{quality}_{base_name}.jpeg"
            output_path = os.path.join(folder_path, output_file_name)

            try:
                # Open the image file
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
                print(f"An error occurred while processing '{file_name}': {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Reduce the size of all PNG or JPEG images in a folder."
    )
    parser.add_argument(
        "input_folder_path", type=str, help="The path to the folder containing images."
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=85,
        help="The quality level for the saved images (1-100).",
    )
    parser.add_argument(
        "--width",
        type=int,
        help="The width to resize the images to. Preserves aspect ratio.",
    )
    parser.add_argument(
        "--height",
        type=int,
        help="The height to resize the images to. Preserves aspect ratio.",
    )

    args = parser.parse_args()
    reduce_image_size_in_folder(
        args.input_folder_path,
        quality=args.quality,
        width=args.width,
        height=args.height,
    )
