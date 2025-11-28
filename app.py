# app.py
import streamlit as st
from config import APP_TITLE, APP_DESCRIPTION
from utils.auth import init_session, login, logout
from services.db import init_db

def main():
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    init_session()
    init_db()

    st.title(APP_TITLE)
    st.write(APP_DESCRIPTION)

    with st.sidebar:
        st.subheader("Login")
        username = st.text_input("Name")
        phone = st.text_input("Phone (for history)", max_chars=15)
        role = st.selectbox("Role", ["farmer", "expert", "admin"])
        if st.button("Login"):
            if role == "admin":
                from config import ADMIN_USERNAME, ADMIN_PASSWORD
                u = st.text_input("Admin username", value=ADMIN_USERNAME, key="admin_u")
                p = st.text_input("Admin password", type="password", key="admin_p")
                if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                    login(username or "Admin", "admin")
                    st.success("Logged in as admin.")
                else:
                    st.error("Invalid admin credentials.")
            else:
                login(username or "Guest", role)
                st.success(f"Logged in as {role}.")
        if st.session_state.get("user"):
            st.info(f"Current user: {st.session_state['user']} ({st.session_state['role']})")
            if st.button("Logout"):
                logout()
                st.experimental_rerun()

    st.markdown("### Modules")
    st.markdown(
        "- 📸 Diagnose Disease: upload images and create reports.\n"
        "- 📊 Farmer History: view past reports by phone number.\n"
        "- 🌍 Outbreak Dashboard: monitor hotspots and trends.\n"
        "- 🧪 Lab Expert Panel: verify cases and add expert notes.\n"
        "- ⚙️ Admin Config: manage system settings."
    )

if __name__ == "__main__":
    main()
