import flet as ft
import numpy as np

from lia import ExtractLeaf, GetFvFm
from lia.basic.thread import WorkingThread
from lia.basic.transform.image import to_base64
from lia.data.color_fvfm import ColorFvFmData
from lia.gui.base.run_tab import RunTab
from lia.gui.widgets.image_container import ImageContainer
from lia.gui.widgets.image_listview import ImageListView
from lia.gui.widgets.slider import BoxSlider

GET_FVFM_TITLE = "Get Fv/Fm value"
DEFAULT_IMAGE_PATH = f"/images/photo.png"
ARROW_IMAGE_PATH = f"/images/arrow.png"
METHOD_IMAGE_PATH = "/images/get_fvfm_method.png"
METHOD_EXPLANATION = "Reads the Fv/Fm scale bar from an image and creates its value and color correspondence table. Also, extract only the leaf area from an image."


class GetFvFmTab(RunTab):
    """ColorFvFm application tab: Get Fv/Fm."""

    def __init__(self, data: ColorFvFmData):
        super().__init__()
        self.data: ColorFvFmData = data
        self.text = GET_FVFM_TITLE
        self.extr = ExtractLeaf()
        self.get_fvfm = GetFvFm()
        self.thresh = self.extr.thresh
        self.default_thresh = self.extr.thresh
        self.set_contents()

    def set_contents(self):
        """Set controls."""
        self.input_image_container = ImageContainer(DEFAULT_IMAGE_PATH)
        self.output_image_container = ImageContainer(DEFAULT_IMAGE_PATH)
        self.list_view = ImageListView(expand=1, spacing=10)
        self.thresh_slider = BoxSlider(self.thresh, max=255, min=0, divisions=255)

        # Layout
        self.content = ft.Container(
            padding=ft.padding.all(10),
            content=ft.Row(
                spacing=10,
                controls=[
                    ft.Container(  # Image area
                        border=ft.border.all(2, ft.colors.WHITE),
                        expand=4,
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
                    ft.Container(  # Fv/Fm value list area
                        border=ft.border.all(2, ft.colors.WHITE),
                        expand=1,
                        padding=ft.padding.all(10),
                        content=ft.Column(
                            controls=[
                                ft.Row(  # List title
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            "Fv/Fm value", expand=1, expand_loose=True
                                        )
                                    ],
                                ),
                                ft.Divider(color=ft.colors.WHITE),
                                ft.Row(  # List view
                                    expand=1,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[self.list_view],
                                ),
                            ],
                            expand=True,
                        ),
                    ),
                    ft.Container(  # Method area
                        border=ft.border.all(2, ft.colors.WHITE),
                        padding=ft.padding.all(10),
                        expand=4,
                        content=ft.Column(
                            expand=1,
                            controls=[
                                ft.Column(
                                    expand=1,
                                    scroll=ft.ScrollMode.ALWAYS,
                                    controls=[
                                        ft.Text(METHOD_EXPLANATION),
                                        ft.Divider(height=1, color=ft.colors.WHITE),
                                        ft.Text("Step 1. Select Image"),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.OutlinedButton(
                                                    "Select Image",
                                                    icon=ft.icons.INSERT_PHOTO_OUTLINED,
                                                    on_click=self.show_select_file_dialog,
                                                    expand=1,
                                                    expand_loose=True,
                                                )
                                            ],
                                        ),
                                        ft.Divider(height=1, color=ft.colors.WHITE),
                                        ft.Text("Step 2. Set threshold for extract"),
                                        ft.Row(
                                            [
                                                ft.OutlinedButton(
                                                    "Reset", on_click=self.reset_thresh
                                                ),
                                                ft.Container(
                                                    expand=1, content=self.thresh_slider
                                                ),
                                            ]
                                        ),
                                        ft.Divider(height=1, color=ft.colors.WHITE),
                                        ft.Text("Step 3. Run"),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.OutlinedButton(
                                                    "RUN",
                                                    expand=1,
                                                    expand_loose=True,
                                                    on_click=self.click_run,
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                                ft.Divider(height=1, color=ft.colors.WHITE),
                                ft.Row(  # Move tab buttons
                                    [
                                        ft.Row(
                                            expand=1,
                                            alignment=ft.MainAxisAlignment.START,
                                            controls=[
                                                ft.OutlinedButton(
                                                    "<- Back",
                                                    expand=1,
                                                    expand_loose=True,
                                                    on_click=self.to_previous_tab,
                                                )
                                            ],
                                        ),
                                        ft.Row(
                                            expand=1,
                                            alignment=ft.MainAxisAlignment.END,
                                            controls=[
                                                ft.OutlinedButton(
                                                    "Next ->",
                                                    expand=1,
                                                    expand_loose=True,
                                                    on_click=self.to_next_tab,
                                                )
                                            ],
                                        ),
                                    ]
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    def select_file(self, e):
        "Select input image file."
        input_path = super().select_file(e)
        self.data.input_fvfm_path = input_path
        self.input_image_container.set_image(input_path, "path")
        self.page.update()

    def reload(self):
        """Reload image, when tab changed."""
        self.input_image_container.set_image(self.data.input_fvfm_path, "path")
        self.output_image_container.set_image(
            self.data.extract_fvfm_img_base64, "base64"
        )
        self.page.update()

    def reset_thresh(self, e):
        """Reset threshold value."""
        self.thresh_slider.set_value(self.default_thresh)

    def click_run(self, e):
        """Running process."""
        if self.data.input_fvfm_path is None:
            self.show_error_dialog("No input image. Please select image file.")
            return
        self.thread = WorkingThread(target=self.run)
        self.thread.start()

    def run(self):
        """Run Extract leaf and Get Fv/Fm value."""
        self.show_progress_dialog("Extract Leaf contours", "Extracting leaf...")
        try:
            thresh = self.thresh_slider.get_value()
            self.extr.set_param(thresh=thresh)
            extr_imgs, extr_cnts = self.extr.get_by_thresh(self.data.input_fvfm_path)
            self.data.extract_fvfm_img = extr_imgs[0]
            self.data.fvfm_cnts = extr_cnts[0]
            self.data.extract_fvfm_img_base64 = to_base64(extr_imgs[0])
            self.output_image_container.set_image(
                self.data.extract_fvfm_img_base64, "base64"
            )
            self.page.update()
            self.page.close(self.dialog)
            self.show_progress_dialog("Get Fv/Fm value", "Reading Fv/Fm value...")
            self.data.fvfm_color_list, self.data.fvfm_value_list = (
                self.get_fvfm.get_list(self.data.input_fvfm_path)
            )
            image_base64_list = []
            for color in self.data.fvfm_color_list:
                image = np.full((24, 24, 3), color, np.uint8)
                image_base64 = to_base64(image)
                image_base64_list.append(image_base64)
            value_list = ["{:.3f}".format(x) for x in self.data.fvfm_value_list]
            self.list_view.append_list(image_base64_list, value_list)
            self.page.update()
            self.page.close(self.dialog)
        except Exception as e:
            self.page.close(self.dialog)
            self.show_error_dialog(str(e))
