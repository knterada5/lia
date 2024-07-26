import flet as ft

from lia.data.color_fvfm import ColorFvFmData
from lia.gui.base.content_tab import ContentTab

GET_FVFM_TITLE = "Get Fv/Fm value"


class GetFvFmTab(ContentTab):
    def __init__(self, data: ColorFvFmData):
        super().__init__()
        self.data = data
        self.text = GET_FVFM_TITLE
        self.set_content()

    def set_content(self):
        self.content = ft.Text(GET_FVFM_TITLE)
