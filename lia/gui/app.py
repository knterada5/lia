import os

import flet as ft

from .color_fvfm.color_fvfm_page import (
    COLOR_FVFM_ROUTE,
    COLOR_FVFM_TITLE,
    ColorFvFmPage,
)

TOP_TITLE = "Leaf Image Analysis"


class Top(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/")
        self.controls = [
            ft.AppBar(title=ft.Text(TOP_TITLE)),
            ft.Text("Applications"),
            ft.ElevatedButton(COLOR_FVFM_TITLE, on_click=self.to_color_fvfm),
        ]
        self.page = page
        self.page.title = TOP_TITLE
        self.page.on_route_change = self.route_change
        self.page.go("/")

    def to_color_fvfm(self, e):
        self.page.go(COLOR_FVFM_ROUTE)

    def route_change(self, route):
        if self.page.route == "/":
            self.page.views.clear()
            self.page.views.append(self)
            self.page.update()
        elif self.page.route == COLOR_FVFM_ROUTE:
            self.page.views.append(ColorFvFmPage(self.page))
            self.page.update()


def application(page: ft.Page):
    Top(page)
