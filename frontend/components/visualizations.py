import streamlit as st

def show_plots(ncfa):
    st.image(f"http://localhost:8000/plots/points_vs_time?ncfa={ncfa}", caption="Points vs Time")