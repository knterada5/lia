import flet as ft

from lia.data.color_fvfm import ColorFvFmData
from lia.gui.base.content_tab import ContentTab

EXTRACT_LEAF_TITLE = "Extract Leaf"


class ExtractLeafTab(ContentTab):
    def __init__(self, data: ColorFvFmData):
        super().__init__()
        self.data = data
        self.text = EXTRACT_LEAF_TITLE
        self.set_content()
        print(data)

    def set_content(self):
        self.content = ft.Text(EXTRACT_LEAF_TITLE)
