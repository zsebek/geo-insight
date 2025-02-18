import streamlit as st

from components.widget_board.factory import WidgetFactory

class BoardContainer:
    def __init__(self):
        self.layout_key = "widget_board_layout"
        if self.layout_key not in st.session_state:
            # TODO: implement add_widget behavior
            st.session_state[self.layout_key] = [
                [{"id": "widget_1", "type": "DataFrameWidget"}],
                [{"id": "widget_2", "type": "InteractiveMapWidget"}],
                []
            ]
    def render(self):
        _, col2 = st.columns([9,1])
        with col2:
            if st.button("Edit layout"):
                st.session_state["edit_mode"] = not st.session_state.get("edit_mode", False)
        
        if st.session_state.get("edit_mode", False):
            self.render_edit_view()
        else:
            self.render_active_region()
    
    def render_active_region(self):
        board_layout = st.session_state[self.layout_key]
        
        columns = st.columns(len([col for col in board_layout if col]))  # Dynamically set columns

        for col_idx, widgets in enumerate(board_layout):
            if widgets:  # Only render non-empty columns
                with columns[col_idx]:
                    for widget_data in widgets:
                        widget = WidgetFactory.create_widget(widget_data["id"], widget_data["type"])
                        widget.render()

    def render_edit_view(self):
        st.subheader("Edit Mode: Drag and Arrange Widgets")

        board_layout = st.session_state[self.layout_key]
        columns = st.columns(3)  # Assuming max 3 columns

        for col_idx, widgets in enumerate(board_layout):
            with columns[col_idx]:
                st.write(f"Column {col_idx + 1}")

                for widget in widgets:
                    widget_label = f"{widget['type']} ({widget['id']})"
                    if st.button(f"✏️ Edit {widget_label}"):
                        st.session_state["edit_widget"] = widget

                    if st.button(f"❌ Remove {widget_label}"):
                        board_layout[col_idx].remove(widget)

        # Button to add new widgets
        if st.button("➕ Add Widget"):
            st.session_state["add_widget"] = True

    def add_widget_modal(self):
        if st.session_state.get("add_widget", False):
            st.write("### Add New Widget")
            widget_type = st.selectbox("Select Widget Type", ["DataframeWidget", "InteractiveMap"])
            widget_id = st.text_input("Widget ID")

            if st.button("Add"):
                st.session_state[self.layout_key][0].append({"id": widget_id, "type": widget_type})
                st.session_state["add_widget"] = False


