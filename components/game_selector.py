import streamlit as st
import requests

def get_game_tokens(ncfa):
    return requests.get(f"http://localhost:8000/games/tokens?ncfa={ncfa}").json()

def game_selector():
    ncfa = st.text_input("Enter NCFA Cookie")
    if ncfa:
        return get_game_tokens(ncfa)
    return None