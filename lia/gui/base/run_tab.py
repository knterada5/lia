import flet as ft


class RunTab(ft.Tab):
    """Base tab."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def show_error_dialog(self, message):
        """Show Error dialog.

        Parameters
        ----------
        message : str
            Error message.
        """
        dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.page.close(dialog))],
        )
        self.page.open(dialog)

    def show_progress_dialog(self, title, message):
        """Show progress dialog.

        Parameters
        ----------
        title : str
            Dialog title.
        message : str
            Progress message.
        """
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[ft.TextButton("Cancel", on_click=self.cancel_job)],
        )
        self.page.open(self.dialog)

    def cancel_job(self, e):
        """Cancel running job."""
        self.page.close(self.dialog)
        try:
            self.thread.raise_exception()
        except Exception as e:
            self.show_error_dialog(str(e))

    def show_select_file_dialog(self, e):
        """Show select file dialog."""
        file_picker = ft.FilePicker(on_result=self.select_file)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files()

    def select_file(self, e):
        """Select file.

        Returns
        -------
        path : str
            Selected file path.
        """
        if e.files is None:
            return
        path = e.files[0].path
        return path

    def to_next_tab(self, e):
        """Move to next tab."""
        self.parent.to_next_tab()

    def to_previous_tab(self, e):
        """Move to previous tab."""
        self.parent.to_previous_tab()
