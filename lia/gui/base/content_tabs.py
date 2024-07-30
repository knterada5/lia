import flet as ft


class ContentTabs(ft.Tabs):
    """Base Tabs."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_next_tab(self):
        """Move to next tab."""
        last_tab = len(self.tabs) - 1
        if self.selected_index == last_tab:
            return
        self.selected_index += 1
        self.update()

    def to_previous_tab(self):
        """Move to previous tab."""
        if self.selected_index == 0:
            return
        self.selected_index -= 1
        self.update()
