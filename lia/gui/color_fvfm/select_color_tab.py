import flet as ft

from lia.data.color_fvfm import ColorFvFmData
from lia.gui.base.content_tab import ContentTab

SELECT_COLOR_TAB = "Select Color"


class SelectColorTab(ContentTab):
    def __init__(self, data: ColorFvFmData):
        super().__init__()
        self.data = data
        self.text = SELECT_COLOR_TAB
        self.set_content()

    def set_content(self):
        self.content = ft.Text(SELECT_COLOR_TAB)
