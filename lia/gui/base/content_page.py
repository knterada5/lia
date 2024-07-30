import flet as ft


class ContentPage(ft.View):
    """Base Page."""

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def click_back_button(self, e):
        """Back to Top."""
        dialog = ft.AlertDialog(
            title=ft.Text("Please confirm"),
            content=ft.Text(
                "If you return to the Top, the entered data will be lost.\nDo you really want to back to the Top?"
            ),
            actions=[
                ft.TextButton("Yes", on_click=lambda e: self.page.go("/")),
                ft.TextButton("No", on_click=lambda e: self.page.close(dialog)),
            ],
        )
        self.page.open(dialog)
