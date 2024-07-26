import flet as ft

from lia.data.color_fvfm import ColorFvFmData
from lia.gui.base.content_tab import ContentTab

MAKE_GRAPH_TITLE = "Graph"


class MakeGraphTab(ContentTab):
    def __init__(self, data: ColorFvFmData):
        super().__init__()
        self.data = data
        self.text = MAKE_GRAPH_TITLE
        self.set_content()

    def set_content(self):
        self.content = ft.Text(MAKE_GRAPH_TITLE)
