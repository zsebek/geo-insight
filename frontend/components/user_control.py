import streamlit as st
from utils.http import get_url, post

def set_active_user():
    _, ok = post(f"auth/active_user?user_name={st.session_state.selected_user}")
    if not ok: st.error("error setting active user from dropdown")
    
    
def render_user_selector():
    """Display user profile selection UI."""
    with st.sidebar:
        handle_auth()
        
        res, ok = get_url("/auth/users")
        if not ok: return
        users = res["data"]
        if not users:
            st.error("No users found. Please update your keys.")
            return

        st.selectbox(
            "Select a user:",
            users,
            index=users.index(st.session_state.active_user) if st.session_state.active_user in users else 0,
            key="selected_user",
            on_change=set_active_user  # Calls function when selection changes
        )


def handle_auth():
    with st.spinner("logging you in"):
        res, ok = get_url("auth/active_user")
        st.session_state.active_user = res['data']
        _, ok = get_url(f"auth/login?user_name={st.session_state.active_user}")
    
    if not ok:
        st.write("couldn't log you in")
