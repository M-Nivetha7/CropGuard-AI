# models/disease_model.py
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np

@dataclass
class PredictionResult:
    disease: str
    confidence: float
    severity: str
    infected: bool
    top_k: List[Tuple[str, float]]

UNKNOWN_LABEL = "Unknown / not a leaf"

# Tuned thresholds
MIN_LEAF_GREEN_RATIO = 0.12      # leaf must have at least 12% green pixels
INFECT_STRONG = 0.06             # >= 6% spots -> definitely infected
INFECT_WEAK = 0.03               # 3–6% spots -> maybe mild infection

def get_model():
    return "SIMPLE_COLOR_MODEL_V2"

def _leaf_and_spot_stats(image_tensor: np.ndarray):
    arr = image_tensor[0]  # H,W,3 in [0,1]
    h, w, _ = arr.shape
    total = h * w

    rgb = (arr * 255).astype(np.uint8)
    r = rgb[:, :, 0].astype(float)
    g = rgb[:, :, 1].astype(float)
    b = rgb[:, :, 2].astype(float)

    # Leaf body = clearly green pixels
    green_mask = (g > 70) & (g > r + 5) & (g > b + 5)
    green_count = np.count_nonzero(green_mask)
    green_ratio = green_count / total

    # Background = very bright or very dark outside likely leaf area
    inside_leaf = (g > 40)
    non_green_inside = inside_leaf & (~green_mask)

    # Dark/brown necrotic pixels
    dark_mask = (r < 110) & (g < 120) & (b < 110)
    # Yellowish lesions (r and g both high but not pure green)
    yellow_mask = (g > 130) & (r > 130) & (b < 140)

    spot_mask = non_green_inside & (dark_mask | yellow_mask)
    spot_count = np.count_nonzero(spot_mask)
    spot_ratio = spot_count / total

    leaf_like = green_ratio >= MIN_LEAF_GREEN_RATIO
    return leaf_like, float(green_ratio), float(spot_ratio)

def predict(image_tensor: np.ndarray, crop: str) -> PredictionResult:
    if image_tensor.ndim != 4:
        raise ValueError("Expected tensor of shape (1, H, W, 3)")

    leaf_like, green_ratio, spot_ratio = _leaf_and_spot_stats(image_tensor)

    # 1) Not a leaf
    if not leaf_like:
        return PredictionResult(
            disease=UNKNOWN_LABEL,
            confidence=1.0,
            severity="N/A",
            infected=False,
            top_k=[(UNKNOWN_LABEL, 1.0)],
        )

    # 2) Leaf detected: decide infection by spot_ratio
    if spot_ratio >= INFECT_STRONG:
        disease_label = "Infected leaf"
        infected = True
        severity = "Severe"
        conf = 0.9
    elif spot_ratio >= INFECT_WEAK:
        disease_label = "Infected leaf"
        infected = True
        severity = "Mild/Moderate"
        conf = 0.7
    else:
        disease_label = "Healthy leaf"
        infected = False
        severity = "None"
        # more green -> more confident healthy
        conf = min(0.5 + green_ratio * 3.0, 0.95)

    return PredictionResult(
        disease=disease_label,
        confidence=float(conf),
        severity=severity,
        infected=infected,
        top_k=[(disease_label, float(conf))],
    )
