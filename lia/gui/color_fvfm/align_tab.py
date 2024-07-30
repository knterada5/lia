import flet as ft

from lia.data.color_fvfm import ColorFvFmData
from lia.gui.base.run_tab import RunTab

ALIGN_TITLE = "Align"


class AlignTab(RunTab):
    def __init__(self, data: ColorFvFmData):
        super().__init__()
        self.data = data
        self.text = ALIGN_TITLE
        self.set_contents()

    def set_contents(self):
        pass

    def reload(self):
        pass
