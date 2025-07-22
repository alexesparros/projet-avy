from PIL import Image
import base64
import os

def check_image_exists(path):
    return os.path.isfile(path)

def img_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

def open_image_safe(path):
    try:
        return Image.open(path).convert("RGBA")
    except FileNotFoundError:
        return None 