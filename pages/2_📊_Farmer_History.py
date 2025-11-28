# pages/2_📊_Farmer_History.py
import streamlit as st
import pandas as pd
from utils.auth import require_login
from services.reporting import get_reports_by_farmer

require_login(roles=["farmer", "admin"])

st.title("📊 My Diagnosis History")

phone = st.text_input("Enter phone number used for reports")
if st.button("Load history") and phone:
    reports = get_reports_by_farmer(phone)
    if not reports:
        st.info("No reports found for this phone.")
    else:
        df = pd.DataFrame(reports)
        st.dataframe(df, use_container_width=True)
        st.download_button("Download CSV", df.to_csv(index=False), "history.csv", "text/csv")
