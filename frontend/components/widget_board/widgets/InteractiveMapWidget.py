import streamlit as st
from components.widget_board.widgets.WidgetBase import WidgetBase

class InteractiveMapWidget(WidgetBase):
    def __init__(self, widget_id: str):
        super().__init__(widget_id, "InteractiveMap")

    def render(self):
        st.write("[Interactive Map Placeholder]")