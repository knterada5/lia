import importlib
import importlib.resources

import flet as ft

from .color_fvfm.color_fvfm_page import (
    COLOR_FVFM_ROUTE,
    COLOR_FVFM_TITLE,
    ColorFvFmPage,
)

# from .color_fvfm_app import COLOR_FVFM_ROUTE, COLOR_FVFM_TITLE, ColorFvFmPage

TOP_TITLE = "Leaf Image Analysis"


class Top(ft.View):
    """Top page."""

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
        """Move to ColorFvFm application."""
        self.page.go(COLOR_FVFM_ROUTE)

    def route_change(self, route):
        """Set view when route change."""
        if self.page.route == "/":
            self.page.views.clear()
            self.page.views.append(self)
            self.page.update()
        elif self.page.route == COLOR_FVFM_ROUTE:
            self.page.views.append(ColorFvFmPage())
            self.page.update()


def application(page: ft.Page):
    """Set application to screen."""
    Top(page)


def run():
    """Run application."""
    path = importlib.resources.files("lia")
    ft.app(target=application, assets_dir=str(path) + "/assets")
