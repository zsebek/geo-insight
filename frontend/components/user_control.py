import streamlit as st
from utils.http import get, post

def set_active_user():
    _, ok = post(f"auth/active_user?user_name={st.session_state.selected_user}")
    if not ok: st.error("error setting active user from dropdown")
    
    
def render_user_selector():
    """Display user profile selection UI."""
    res, ok = get("/auth/users")
    if not ok: return
    users = res['data']
    if not users: st.error("No users found, pelase update your keys.")
    st.selectbox(
        "Select a user:",
        users,
        index=users.index(st.session_state.active_user) if st.session_state.active_user in users else 0,
        key="selected_user",
        on_change=set_active_user  # Calls function when selection changes
    )
    