# models/__init__.py
from .disease_model import get_model, predict, PredictionResult
from .risk_model import compute_risk_score, RiskFactors

__all__ = [
    "get_model",
    "predict",
    "PredictionResult",
    "compute_risk_score",
    "RiskFactors",
]
