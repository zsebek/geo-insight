import streamlit as st
import requests

st.title("GeoInsight")

ncfa = st.text_input("Enter NCFA Cookie")

if ncfa:
    response = requests.get(f"http://localhost:8000/auth/session?ncfa={ncfa}")
    if response.status_code == 200:
        st.success("Authentication successful!")
        game_tokens = requests.get(f"http://localhost:8000/games/tokens?ncfa={ncfa}").json()
        num_games = st.slider("Select number of games", 10, 400, 50)
        if st.button("Analyze"):
            stats = requests.get(f"http://localhost:8000/stats/calculate?ncfa={ncfa}&num_games={num_games}").json()
            st.write(stats)
            st.image(f"http://localhost:8000/plots/points_vs_time?ncfa={ncfa}", caption="Points vs Time")