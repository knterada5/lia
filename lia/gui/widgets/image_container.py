import flet as ft


class ImageContainer(ft.Row):
    """Image container."""

    def __init__(self, default_img):
        super().__init__()
        self.expand = True
        self.alignment = ft.alignment.center
        self.image = ft.Image(src=default_img, expand=1)
        self.controls = [self.image]

    def set_image(self, input, input_type):
        """Set Image.

        Parameters
        ----------
        input : str
            Input image path.
        input_type : str
            Input image by base64 format.
        """
        if input is None:
            return
        if input_type == "path":
            self.image.src = input
        elif input_type == "base64":
            self.image.src_base64 = input
