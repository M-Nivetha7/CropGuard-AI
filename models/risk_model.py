# models/risk_model.py
from dataclasses import dataclass

@dataclass
class RiskFactors:
    rain_mm: float          # recent rainfall
    humidity: int           # relative humidity %
    crop_stage: str         # e.g. "Seedling", "Vegetative", "Flowering", "Maturity"
    previous_outbreaks: int # number of recent cases nearby
    severity_weight: float  # base weight from model severity (0–1)

def compute_risk_score(factors: RiskFactors) -> float:
    """
    Heuristic risk score 0–1 using simple weighted features.
    You can later replace this with a trained model.
    """
    # normalize features
    rain_term = min(factors.rain_mm / 80.0, 1.0)          # heavy rain → higher risk
    hum_term = min(max(factors.humidity, 0), 100) / 100.0
    prev_term = min(factors.previous_outbreaks / 10.0, 1.0)

    stage_weight = {
        "Seedling": 0.6,
        "Vegetative": 1.0,
        "Flowering": 1.2,
        "Maturity": 0.7,
    }.get(factors.crop_stage, 0.8)

    base = (
        0.25 * rain_term
        + 0.25 * hum_term
        + 0.25 * prev_term
        + 0.25 * factors.severity_weight
    ) * stage_weight

    return max(0.0, min(round(base, 2), 1.0))
