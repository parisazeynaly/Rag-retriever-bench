from PIL import Image
import numpy as np
from typing import List

def color_histogram(path: str, bins: int = 16) -> List[float]:
    img = Image.open(path).convert("RGB").resize((128, 128))
    arr = np.asarray(img).reshape(-1, 3)
    hist = []
    for c in range(3):
        h, _ = np.histogram(arr[:, c], bins=bins, range=(0, 255), density=True)
        hist.extend(h.tolist())
    return (np.asarray(hist) / (np.linalg.norm(hist) + 1e-9)).tolist()
