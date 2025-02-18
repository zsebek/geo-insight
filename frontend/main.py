import streamlit as st

# TODO: make user selector 
active_user = "Zach"
st.set_page_config(layout="wide")
home_page = st.Page("pages/home.py", title=f"{active_user}'s GeoCoach", icon=":material/globe_location_pin:")
tactical_page = st.Page("pages/tactical.py", title="Tactical Analytics Dashboard", icon=":material/analytics:")

pg = st.navigation(
    {
        "": [home_page],
		"Analysis": [tactical_page],
	}
)

pg.run()