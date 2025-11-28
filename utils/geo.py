# utils/geo.py
from typing import Tuple

def parse_latlon(lat_str: str, lon_str: str) -> Tuple[float, float] | None:
    try:
        return float(lat_str), float(lon_str)
    except (TypeError, ValueError):
        return None

def district_to_fake_coords(district: str) -> Tuple[float, float]:
    # simple hash → coordinates (demo only)
    base_lat = 20.5
    base_lon = 78.9
    h = abs(hash(district)) % 1000
    return base_lat + (h % 50) * 0.01, base_lon + (h // 50) * 0.01
