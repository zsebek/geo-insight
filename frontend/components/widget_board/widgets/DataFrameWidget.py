import streamlit as st
from components.widget_board.widgets.WidgetBase import WidgetBase

class DataFrameWidget(WidgetBase):
    def __init__(self, widget_id: str):
        super().__init__(widget_id, "DataframeWidget")
        # TODO: fetch data on render
    
    @st.cache_data
    def get_data():
        pass

    def render(self):
        st.write("Data frame sorting and filtering form / interactive buttons")
        st.write("Dataframe displaying raw data")
