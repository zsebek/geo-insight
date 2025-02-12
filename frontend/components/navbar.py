import streamlit as st

def remove_tab(tab_index):
    """Removes a tab from the list when 'X' is clicked."""
    if len(st.session_state["tabs"]) > 1:  # Prevent removing the last tab
        del st.session_state["tabs"][tab_index]

def add_tab():
    """Adds a new tab to the tab list."""
    new_tab = f"Tab {len(st.session_state['tabs'])+1}"
    st.session_state["tabs"].append(new_tab)

def render_navbar():
    """Creates a horizontal tab navbar with close buttons."""
    
    # ✅ Ensure session state variables exist
    if "tabs" not in st.session_state:
        st.session_state["tabs"] = ["Dashboard", "Analysis", "Raw Data"]
    if "active_tab" not in st.session_state:
        st.session_state["active_tab"] = "Dashboard"

    # ✅ Create a horizontal row for tabs
    tab_columns = st.columns(len(st.session_state["tabs"]) + 1, gap='small')  # Extra column for "+"

    # ✅ Display tabs with close buttons
    for i, tab_name in enumerate(st.session_state["tabs"]):
        with tab_columns[i]:
            if st.button(f"❌ {tab_name}", key=f"close_{i}"):
                remove_tab(i)
                st.rerun()  # Refresh UI after removing tab

    # ✅ Add "➕ Add Tab" button at the end
    with tab_columns[-1]:
        if st.button("➕", key="add_tab"):
            add_tab()
            st.rerun()  # Refresh UI after adding a tab

    # ✅ Ensure active_tab remains valid after modifications
    if st.session_state["active_tab"] not in st.session_state["tabs"]:
        st.session_state["active_tab"] = st.session_state["tabs"][0]

