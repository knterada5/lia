import flet as ft

from lia.data.color_fvfm import ColorFvFmData
from lia.gui.base.content_page import ContentPage

from .align_tab import ALIGN_TITLE, AlignTab
from .auto_tab import AUTO_TITLE, AutoTab
from .extract_leaf_tab import EXTRACT_LEAF_TITLE, ExtractLeafTab
from .get_fvfm_tab import GET_FVFM_TITLE, GetFvFmTab
from .make_graph_tab import MAKE_GRAPH_TITLE, MakeGraphTab
from .select_color_tab import SELECT_COLOR_TAB, SelectColorTab

COLOR_FVFM_ROUTE = "/color_fvfm"
COLOR_FVFM_TITLE = "Make Graph: Leaf Color and Fv/Fm"


class ColorFvFmPage(ContentPage):
    def __init__(self, page: ft.Page):
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
        self.page = page


class ColorFvFmTabs(ft.Tabs):
    def __init__(self):
        super().__init__(data=ColorFvFmData(), selected_index=0, animation_duration=400)
        self.tab0 = ExtractLeafTab(self.data)
        self.tab1 = GetFvFmTab(self.data)
        self.tab2 = AlignTab(self.data)
        self.tab3 = SelectColorTab(self.data)
        self.tab4 = MakeGraphTab(self.data)
        self.tab5 = AutoTab(self.data)
        self.tabs = [self.tab0, self.tab1, self.tab2, self.tab3, self.tab4, self.tab5]
        self.on_change = self.change

    def change(self, e):
        if self.selected_index == 0:
            self.tab0.update()
        elif self.selected_index == 1:
            self.tab1.update()
        elif self.selected_index == 2:
            self.tab2.update()
        elif self.selected_index == 3:
            self.tab3.update()
        elif self.selected_index == 4:
            self.tab4.update()
        elif self.selected_index == 5:
            self.tab5.update()
