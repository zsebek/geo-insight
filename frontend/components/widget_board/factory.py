from components.widget_board.widgets.DataFrameWidget import DataFrameWidget
from components.widget_board.widgets.InteractiveMapWidget import InteractiveMapWidget
from components.widget_board.widgets.WidgetBase import WidgetBase
# Widget Factory for dynamic creation
class WidgetFactory:
    @staticmethod
    def create_widget(widget_id: str, widget_type: str):
        if widget_type == "DataFrameWidget":
            return DataFrameWidget(widget_id)
        elif widget_type == "InteractiveMapWidget":
            return InteractiveMapWidget(widget_id)
        return WidgetBase(widget_id, "Unknown")