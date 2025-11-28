# utils/image_utils.py

from PIL import Image, ImageOps
import numpy as np

def load_image(file) -> Image.Image:
    """
    Load an uploaded/captured image and convert it to RGB.
    """
    return Image.open(file).convert("RGB")

def preprocess_image(img: Image.Image, size=(224, 224)) -> Image.Image:
    """
    Apply basic preprocessing:
    - Fix orientation using EXIF
    - Resize to the target size expected by the model
    """
    img = ImageOps.exif_transpose(img)
    img = img.resize(size)
    return img

def to_model_tensor(img: Image.Image) -> np.ndarray:
    """
    Convert a PIL image to a model-ready tensor:
    - Shape: (1, H, W, 3)
    - Type: float32
    - Range: [0, 1]
    """
    arr = np.array(img).astype("float32") / 255.0   # H, W, 3
    arr = np.expand_dims(arr, axis=0)               # 1, H, W, 3
    return arr
