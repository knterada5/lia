import flet as ft

from lia.data.color_fvfm import ColorFvFmData
from lia.gui.base.content_tab import ContentTab

AUTO_TITLE = "Auto"


class AutoTab(ContentTab):
    def __init__(self, data: ColorFvFmData):
        super().__init__()
        self.data = data
        self.text = AUTO_TITLE
        self.set_content()

    def set_content(self):
        self.content = ft.Text(AUTO_TITLE)
