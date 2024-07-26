import flet as ft


class ContentTab(ft.Tab):
    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def set_content(self):
        pass

    def update(self):
        self.set_content()
        super().update()
