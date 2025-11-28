# pages/5_⚙️_Admin_Config.py
import streamlit as st
from utils.auth import require_login, is_admin
from services.advisory import get_catalog

require_login(roles=["admin"])

st.title("⚙️ Admin & Config")

if not is_admin():
    st.error("Only admin can access this page.")
    st.stop()

st.subheader("Disease catalog (read-only demo)")
catalog = get_catalog()
if not catalog:
    st.info("No catalog loaded. Add entries to data/disease_catalog.json.")
else:
    for name, info in catalog.items():
        with st.expander(name):
            st.write("Description:", info.get("description"))
            st.write("Management:", info.get("management"))
