import flet as ft

from lia.data.color_fvfm import ColorFvFmData
from lia.gui.base.run_tab import RunTab

SELECT_COLOR_TAB = "Select Color"


class SelectColorTab(RunTab):
    def __init__(self, data: ColorFvFmData):
        super().__init__()
        self.data = data
        self.text = SELECT_COLOR_TAB
        self.set_contents()

    def set_contents(self):
        pass

    def reload(self):
        pass
