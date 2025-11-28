# services/weather.py
import random
from typing import Dict

def get_weather_and_risk(district: str, crop: str) -> Dict:
    # In a real app call an API; here use heuristics.
    risk = random.uniform(0.1, 0.9)
    return {
        "district": district,
        "crop": crop,
        "rain_mm": round(random.uniform(0, 80), 1),
        "humidity": random.randint(40, 95),
        "risk_score": round(risk, 2)
    }
