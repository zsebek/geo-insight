import streamlit as st
import pandas as pd
from utils.http import get

def render_timeboard():
    """Displays a raw data table with filtering capabilities."""
    st.subheader("Raw Data Analysis")

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_game = st.selectbox("Select Game Mode", ["All", "Standard", "Duels"])
    with col2:
        sort_by = st.selectbox("Sort By", ["Points", "Time Spent"])
    with col3:
        date_range = st.date_input("Select Date Range", [])

    st.markdown("---")

    # Fetch raw game data
    res, ok = get("data/games/get/all")
    if not ok:
        st.error("Error fetching game data")
        return
    df = pd.DataFrame(res)
    # Apply filters
    if selected_game != "All":
        df = df[df["game_mode"] == selected_game]

    if sort_by == "Points":
        df = df.sort_values("points", ascending=False)
    elif sort_by == "Time Spent":
        df = df.sort_values("time_limit", ascending=True)

    st.dataframe(df)  # Show data table
