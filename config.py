# config.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "farmers_portal.db"

APP_TITLE = "Farmers Disease Diagnostic & Reporting Portal"
APP_DESCRIPTION = "AI-based crop disease diagnosis, reporting and outbreak monitoring."

ADMIN_USERNAME = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASS", "admin123")

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "DUMMY_KEY")
