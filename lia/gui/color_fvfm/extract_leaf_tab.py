import flet as ft

from lia import ExtractLeaf
from lia.basic.thread import WorkingThread
from lia.basic.transform.image import to_base64
from lia.data.color_fvfm import ColorFvFmData
from lia.gui.base.run_tab import RunTab
from lia.gui.widgets.image_container import ImageContainer
from lia.gui.widgets.slider import BoxSlider

EXTRACT_LEAF_TITLE = "Extract Leaf"
DEFAULT_IMAGE_PATH = f"/images/photo.png"
ARROW_IMAGE_PATH = f"/images/arrow.png"
METHOD_IMAGE_PATH = f"/images/extract_leaf_method.png"


class ExtractLeafTab(RunTab):
    """ColorFvFm application tab: Extract leaf."""

    def __init__(self, data: ColorFvFmData):
        super().__init__()
        self.data: ColorFvFmData = data
        self.text = EXTRACT_LEAF_TITLE
        self.extr = ExtractLeaf()
        self.thresh = self.extr.thresh
        self.default_thresh = self.extr.thresh
        self.set_contents()

    def set_contents(self):
        """Set controls."""
        self.input_image_container = ImageContainer(DEFAULT_IMAGE_PATH)
        self.output_image_container = ImageContainer(DEFAULT_IMAGE_PATH)
        self.thresh_slider = BoxSlider(self.thresh, min=0, max=255, divisions=255)
        # Layout
        self.content = ft.Container(
            padding=ft.padding.all(10),
            content=ft.Row(
                [
                    ft.Container(  # Image container.
                        border=ft.border.all(2, ft.colors.WHITE),
                        expand=1,
                        padding=ft.padding.all(10),
                        content=ft.Column(
                            [
                                ft.Container(  # Input image
                                    expand=5, content=self.input_image_container
                                ),
                                ft.Row(  # Arrow
                                    expand=1,
                                    alignment=ft.alignment.center,
                                    controls=[ft.Image(expand=1, src=ARROW_IMAGE_PATH)],
                                ),
                                ft.Container(  # Output image
                                    expand=5, content=self.output_image_container
                                ),
                            ],
                        ),
                    ),
                    ft.Container(  # Method area
                        border=ft.border.all(2, ft.colors.WHITE),
                        expand=1,
                        padding=ft.padding.all(10),
                        content=ft.Column(
                            scroll=ft.ScrollMode.ALWAYS,
                            controls=[
                                ft.Row(  # Method title
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("Method"),
                                    ],
                                ),
                                ft.Row(  # Method image
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Image(src=METHOD_IMAGE_PATH, expand=1)
                                    ],
                                ),
                                ft.Text(  # Method explanation
                                    "Detect leaf outlines from an image. And remove background."
                                ),
                                ft.Text("Step 1. Select Image"),
                                ft.Row(  # Select image button
                                    alignment=ft.MainAxisAlignment.END,
                                    controls=[
                                        ft.TextButton(
                                            "Select Image",
                                            icon=ft.icons.INSERT_PHOTO_OUTLINED,
                                            on_click=self.show_select_file_dialog,
                                        ),
                                    ],
                                ),
                                ft.Text("Step 2. Set threshold for extract"),
                                ft.Row(  # Threshold slider
                                    [
                                        ft.TextButton(  # Resetbutton
                                            "Reset", on_click=self.reset_thresh
                                        ),
                                        ft.Container(  # Slider
                                            expand=1,
                                            content=self.thresh_slider,
                                        ),
                                    ]
                                ),
                                ft.Text("Step 3. Run"),
                                ft.Row(  # Run button
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.TextButton(
                                            "RUN", on_click=self.run, expand=1
                                        ),
                                    ],
                                ),
                                ft.Row(  # Next tab button
                                    alignment=ft.MainAxisAlignment.END,
                                    controls=[
                                        ft.TextButton(
                                            "Next ->", on_click=self.to_next_tab
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ),
                ],
                expand=True,
            ),
        )

    def reset_thresh(self, e):
        """Reset threshold value."""
        self.thresh_slider.set_value(self.default_thresh)

    def select_file(self, e):
        """Select input image file."""
        input_path = super().select_file(e)
        self.data.input_leaf_path = input_path
        self.input_image_container.set_image(input_path, "path")
        self.page.update()

    def reload(self):
        """Reload image, when tab changed."""
        self.input_image_container.set_image(self.data.input_leaf_path, "path")
        self.output_image_container.set_image(
            self.data.extract_leaf_img_base64, "base64"
        )
        self.page.update()

    def run(self, e):
        """Running process."""
        if self.data.input_leaf_path is None:
            self.show_error_dialog("No input image. Please select image file.")
            return
        self.thread = WorkingThread(target=self.run_process)
        self.thread.start()

    def run_process(self):
        """Run extract leaf."""
        self.show_progress_dialog("Extract Leaf", "Running...")
        thresh = self.thresh_slider.get_value()
        self.extr.set_param(thresh=thresh)
        extr_imgs, extr_cnts = self.extr.get_by_thresh(self.data.input_leaf_path)
        self.data.extract_leaf_img = extr_imgs[0]
        self.data.leaf_cnts = extr_cnts[0]
        extr_img_base64 = to_base64(extr_imgs[0])
        self.output_image_container.set_image(extr_img_base64, "base64")
        self.page.update()
        self.page.close(self.dialog)
