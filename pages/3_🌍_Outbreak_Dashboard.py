# pages/3_🌍_Outbreak_Dashboard.py
import streamlit as st
import pandas as pd
from utils.auth import require_login
from services.reporting import list_reports

require_login(roles=["expert", "admin"])

st.title("🌍 Outbreak Dashboard")

reports = list_reports()
if not reports:
    st.info("No reports yet.")
    st.stop()

df = pd.DataFrame(reports)
st.subheader("Overall summary")
st.write(df[["crop", "predicted_disease", "district", "status"]].head())

col1, col2 = st.columns(2)
with col1:
    st.bar_chart(df["predicted_disease"].value_counts())
with col2:
    st.bar_chart(df["district"].value_counts())

if {"latitude", "longitude"}.issubset(df.columns):
    loc_df = df.dropna(subset=["latitude", "longitude"])[["latitude", "longitude"]]
    if not loc_df.empty:
        st.subheader("Spatial distribution")
        st.map(loc_df)
