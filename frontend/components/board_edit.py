import streamlit as st
def render_edit_mode():
    """Allows users to change board layout dynamically."""
    st.subheader("Edit Board Layout")

    layout_options = {
        "1 Column": 1,
        "2 Columns": 2,
        "3 Columns": 3
    }

    selected_layout = st.radio("Choose Layout", list(layout_options.keys()))

    # Store layout choice
    st.session_state["board_layout"] = layout_options[selected_layout]

    st.success(f"Board updated to {selected_layout} layout.")
