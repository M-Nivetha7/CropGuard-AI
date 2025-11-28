# services/db.py
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from config import DB_PATH

Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

def init_db():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT,
            phone TEXT,
            crop TEXT,
            variety TEXT,
            district TEXT,
            latitude REAL,
            longitude REAL,
            image_path TEXT,
            predicted_disease TEXT,
            confidence REAL,
            severity TEXT,
            risk_score REAL,
            advisory TEXT,
            status TEXT DEFAULT 'OPEN',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()
