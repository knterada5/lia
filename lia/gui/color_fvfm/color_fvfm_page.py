import flet as ft

from lia.data.color_fvfm import ColorFvFmData
from lia.gui.base.content_page import ContentPage
from lia.gui.base.content_tabs import ContentTabs

from .align_tab import AlignTab
from .auto_tab import AutoTab
from .extract_leaf_tab import ExtractLeafTab
from .get_fvfm_tab import GetFvFmTab
from .make_graph_tab import MakeGraphTab
from .select_color_tab import SelectColorTab

COLOR_FVFM_ROUTE = "/color_fvfm"
COLOR_FVFM_TITLE = "Make Graph: Leaf Color and Fv/Fm"


class ColorFvFmPage(ContentPage):
    """Application Top page: Draw graph of leaf color and Fv/Fm value."""

    def __init__(self):
        super().__init__(route=COLOR_FVFM_ROUTE)
        self.controls = [
            ft.AppBar(
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK, on_click=self.click_back_button
                ),
                title=ft.Text(COLOR_FVFM_TITLE),
                automatically_imply_leading=False,
            ),
            ColorFvFmTabs(),
        ]


class ColorFvFmTabs(ContentTabs):
    """ColorFvFm application tab."""

    def __init__(self):
        super().__init__(
            data=ColorFvFmData(),
            selected_index=0,
            animation_duration=0,
        )
        self.tab0 = ExtractLeafTab(self.data)
        self.tab1 = GetFvFmTab(self.data)
        self.tab2 = AlignTab(self.data)
        self.tab3 = SelectColorTab(self.data)
        self.tab4 = MakeGraphTab(self.data)
        self.tab5 = AutoTab(self.data)
        self.tabs = [
            self.tab0,
            self.tab1,
            self.tab2,
            self.tab3,
            self.tab4,
            self.tab5,
        ]
        self.on_change = self.change
        self.expand = True

    def change(self, e):
        """Update view, when tab changed."""
        if self.selected_index == 0:
            self.tab0.reload()
        elif self.selected_index == 1:
            self.tab1.reload()
        elif self.selected_index == 2:
            self.tab2.reload()
        elif self.selected_index == 3:
            self.tab3.reload()
        elif self.selected_index == 4:
            self.tab4.reload()
        elif self.selected_index == 5:
            self.tab5.reload()
