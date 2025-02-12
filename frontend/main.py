import streamlit as st
from utils.http import get
from components.user_control import render_user_selector
from components.app_background import app_background
from components.timeboard_layout import render_timeboard
from components.board_edit import render_edit_mode
from components.board_layout import render_board_layout

app_background()
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Dashboard"

# ✅ Use `st.session_state["active_tab"]` without modifying it
if st.session_state["active_tab"] == "Raw Data":
    render_timeboard()
elif st.session_state.get("edit_mode", False):
    render_edit_mode()
else:
    render_board_layout()
