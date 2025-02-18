from abc import ABC, abstractmethod

class WidgetBase(ABC):
    def __init__(self, widget_id: str, widget_type: str):
        self.widget_id = widget_id
        self.widget_type = widget_type

    @abstractmethod
    def render(self):
        pass