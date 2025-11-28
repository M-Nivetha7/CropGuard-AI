# services/advisory.py
import json
from pathlib import Path
from typing import Dict
from config import DATA_DIR
from models.disease_model import UNKNOWN_LABEL

CATALOG_PATH = DATA_DIR / "disease_catalog.json"

def load_catalog() -> Dict:
    if not CATALOG_PATH.exists():
        return {}
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

_catalog = None

def get_catalog():
    global _catalog
    if _catalog is None:
        _catalog = load_catalog()
    return _catalog

def generate_advisory(disease: str, severity: str) -> str:
    """
    Look up a disease in the catalog and build a human-readable advisory.
    Includes special handling when the model says the image is not a crop / unknown.
    """
    # Special case: image does not look like a crop / leaf
    if disease == UNKNOWN_LABEL:
        return (
            "The system could not confidently detect a crop disease from this image.\n\n"
            "Please ensure the photo clearly shows the affected leaf or plant, "
            "avoid documents or backgrounds, and try again."
        )

    catalog = get_catalog()
    entry = catalog.get(disease, {})

    base = entry.get(
        "description",
        "Suspected disease based on visual symptoms."
    )
    mgmt = entry.get(
        "management",
        "Consult your local agronomy officer for detailed advice."
    )

    severity_note = {
        "Mild": "Monitor daily and treat only if symptoms spread.",
        "Moderate": "Start recommended control measures within 24–48 hours.",
        "Severe": "Urgent: treat immediately and consider removing heavily affected plants.",
    }.get(severity, "")

    return f"{base}\n\nRecommended management: {mgmt}\n\nSeverity guidance: {severity_note}"
