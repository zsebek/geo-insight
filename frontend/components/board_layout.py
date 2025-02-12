import streamlit as st
from components.timeboard_layout import render_timeboard

def render_board_layout():
    """Displays board layout with title, edit button, and quick bar."""
    col1, col2 = st.columns([8, 2])

    with col1:
        st.subheader(st.session_state["active_tab"])

    with col2:
        if st.button("Edit Board"):
            st.session_state["edit_mode"] = not st.session_state.get("edit_mode", False)

    st.divider()

    # Quick Analysis Bar
    st.write("Filtering, Sorting, Time range selectors")
    st.divider()
    render_timeboard()
