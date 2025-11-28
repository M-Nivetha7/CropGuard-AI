# utils/auth.py
import streamlit as st

def init_session():
    if "user" not in st.session_state:
        st.session_state.user = None
        st.session_state.role = None

def login(username: str, role: str):
    st.session_state.user = username
    st.session_state.role = role

def logout():
    for key in ["user", "role"]:
        if key in st.session_state:
            del st.session_state[key]

def require_login(roles=None):
    roles = roles or []
    if st.session_state.get("user") is None:
        st.warning("Please log in from the home page.")
        st.stop()
    if roles and st.session_state.get("role") not in roles:
        st.error("You are not authorized to access this page.")
        st.stop()

def is_admin():
    return st.session_state.get("role") == "admin"
