# services/reporting.py
from typing import List, Dict, Any, Optional
from services.db import get_conn

def create_report(payload: Dict[str, Any]) -> int:
    fields = (
        "farmer_name, phone, crop, variety, district, latitude, longitude,"
        " image_path, predicted_disease, confidence, severity, risk_score, advisory, status"
    )
    values = tuple(
        payload.get(k) for k in
        ["farmer_name", "phone", "crop", "variety", "district",
         "latitude", "longitude", "image_path",
         "predicted_disease", "confidence", "severity",
         "risk_score", "advisory", "status"]
    )
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO reports ({fields}) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", values)
        conn.commit()
        return cur.lastrowid

def list_reports(limit: int = 500) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM reports ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        return [dict(r) for r in rows]

def get_reports_by_farmer(phone: str) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM reports WHERE phone = ? ORDER BY created_at DESC", (phone,))
        return [dict(r) for r in cur.fetchall()]

def update_status(report_id: int, status: str):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE reports SET status = ? WHERE id = ?", (status, report_id))
        conn.commit()
