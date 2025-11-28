# pages/4_🧪_Lab_Expert_Panel.py
import streamlit as st
import pandas as pd
from utils.auth import require_login
from services.reporting import list_reports, update_status

require_login(roles=["expert", "admin"])

st.title("🧪 Lab Expert Verification")

reports = list_reports()
if not reports:
    st.info("No reports to verify.")
    st.stop()

df = pd.DataFrame(reports)
open_df = df[df["status"] == "OPEN"]

st.subheader("Open reports")
st.dataframe(open_df[["id", "farmer_name", "phone", "crop", "predicted_disease", "severity"]])

rid = st.number_input("Report ID to verify", min_value=1, step=1)
new_status = st.selectbox("New status", ["OPEN", "CONFIRMED", "REJECTED", "IN_PROGRESS"])
if st.button("Update status"):
    update_status(int(rid), new_status)
    st.success("Status updated. Refresh page to see changes.")
