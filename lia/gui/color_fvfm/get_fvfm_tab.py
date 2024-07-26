import flet as ft

from lia.data.color_fvfm import ColorFvFmData
from lia.gui.base.run_tab import RunTab

GET_FVFM_TITLE = "Get Fv/Fm value"


class GetFvFmTab(RunTab):
    def __init__(self, data: ColorFvFmData):
        super().__init__()
        self.data = data
        self.text = GET_FVFM_TITLE
        self.set_contents()

    def set_contents(self):
        pass

    def input_img(self, path):
        self.data.input_fvfm_path = path

    def reload(self):
        pass
