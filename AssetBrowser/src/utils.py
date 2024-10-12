import os
from PIL import Image

def generate_thumbnail(input_path, output_path, size=(128, 128)):
    with Image.open(input_path) as img:
        img.thumbnail(size)
        img.save(output_path, "PNG")
