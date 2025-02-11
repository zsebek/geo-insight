import streamlit as st
import requests

def display_stats(ncfa, num_games):
    stats = requests.get(f"http://localhost:8000/stats/calculate?ncfa={ncfa}&num_games={num_games}").json()
    st.write(stats)