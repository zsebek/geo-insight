import streamlit as st
from components.user_control import render_user_selector
from components.navbar import render_navbar
from components.user_control import handle_auth


def app_background():
    st.set_page_config(layout="wide", page_title="GeoCoach")
    # Top control bar (Profile + Tabs)
    col1, col2 = st.columns([3, 1])  # Tabs take more space, profile takes less

    with col1:
        render_navbar()  # Tabs at the top

    with col2:        
        render_user_selector()  # Profile selector on the top-right
