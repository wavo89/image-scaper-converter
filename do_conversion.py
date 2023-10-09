import os
from PIL import Image

# Define paths
original_dir = "./original"
converted_dir = "./converted"
# reduce_factor = 0.12
# likely use .1 when using images of size similar to browser
# and dont need to be zoomed to be full, thus needing less quality
reduce_factor = 0.1
# converted_dir = "./extra-converted"
# reduce_factor = 0.01

# Create the converted directory if it doesn't exist
if not os.path.exists(converted_dir):
    os.makedirs(converted_dir)

# List all files in the original directory
file_list = os.listdir(original_dir)

# Process each file
for file_name in file_list:
    # Only process .png files
    if file_name.lower().endswith(".png"):
        # Define the full path for input and output
        input_path = os.path.join(original_dir, file_name)
        output_name = (
            os.path.splitext(file_name)[0] + ".jpg"
        )  # Change extension to .jpg
        output_path = os.path.join(converted_dir, output_name)

        # Open the image
        with Image.open(input_path) as img:
            # Target roughly 20% of the original size
            target_size = os.path.getsize(input_path) * reduce_factor
            quality = 95

            # Iteratively reduce quality to reach target size
            while quality > 10:
                # Use in-memory bytes buffer to get the size without saving the file
                from io import BytesIO

                buf = BytesIO()
                img.save(buf, format="JPEG", quality=quality)
                if buf.tell() <= target_size:
                    break
                quality -= 5

            # Save with the determined quality
            img.save(output_path, format="JPEG", quality=quality)

        print(f"Converted {file_name} to {output_name} with quality {quality}.")

print("Conversion completed!")
