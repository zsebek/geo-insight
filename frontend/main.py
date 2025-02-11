import streamlit as st
from utils.http import get
from components.user_control import render_user_selector

st.title("GeoCoach")
st.divider()

with st.spinner("logging you in"):
    res, ok = get("auth/active_user")
    st.session_state.active_user = res['data']
    _, ok = get(f"auth/login?user_name={st.session_state.active_user}")
    
if not ok:
    st.write("couldn't log you in")
else:
    render_user_selector()