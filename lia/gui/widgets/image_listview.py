import flet as ft


class ImageListView(ft.ListView):
    """List view: Image and Text."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def append_list(self, image_list, text_list):
        """Append list to listview.

        Parameters
        ----------
        image_list : list
            List of images.
        text_list : list
            List of text.

        Raises
        ------
        ValueError
            If the length of the lists are different.
        """
        if len(image_list) != len(text_list):
            raise ValueError("List length is incorrect.")
        for image, text in zip(image_list, text_list):
            control = ft.Row(
                spacing=20,
                controls=[
                    ft.Image(src_base64=image),
                    ft.Row(
                        expand=1,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[ft.Text(text, text_align=ft.TextAlign.CENTER)],
                    ),
                ],
            )
            self.controls.append(control)
