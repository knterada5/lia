import flet as ft

from lia import AlignLeaf
from lia.data.color_fvfm import ColorFvFmData
from lia.gui.base.run_tab import RunTab
from lia.gui.widgets.image_container import ImageContainer

ALIGN_TITLE = "Align"
DEFAULT_IMAGE_PATH = "/images/photo.png"
METHOD_IMAGE_PATH = "/images/align_method.png"
METHOD_EXPLANATION = "Adjust the size and tilt so that the two images overlap exactly."


class AlignTab(RunTab):
    def __init__(self, data: ColorFvFmData):
        super().__init__()
        self.data: ColorFvFmData = data
        self.text = ALIGN_TITLE
        self.align = AlignLeaf()
        self.set_contents()

    def set_contents(self):
        self.leaf_img = ImageContainer(DEFAULT_IMAGE_PATH)
        self.fvfm_img = ImageContainer(DEFAULT_IMAGE_PATH)
        self.aligned_leaf_img = ImageContainer(DEFAULT_IMAGE_PATH)
        self.aligned_fvfm_img = ImageContainer(DEFAULT_IMAGE_PATH)
        self.overlay_img = ImageContainer(DEFAULT_IMAGE_PATH)
        self.content = ft.Container(
            padding=ft.padding.all(10),
            content=ft.Row(
                spacing=10,
                controls=[
                    ft.Container(  # Image area
                        border=ft.border.all(2, ft.colors.WHITE),
                        expand=2,
                        padding=ft.padding.all(10),
                        content=ft.Column(
                            expand=1,
                            controls=[
                                ft.Row(
                                    expand=1, controls=[self.leaf_img, self.fvfm_img]
                                ),
                                ft.Row(
                                    expand=1,
                                    controls=[
                                        self.aligned_leaf_img,
                                        self.aligned_fvfm_img,
                                    ],
                                ),
                                ft.Row(
                                    expand=1,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[self.overlay_img],
                                ),
                            ],
                        ),
                    ),
                    ft.Container(  # Method area
                        border=ft.border.all(2, ft.colors.WHITE),
                        expand=1,
                        padding=ft.padding.all(10),
                        content=ft.Column(
                            expand=1,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[ft.Text("Method")],
                                ),
                                ft.Column(
                                    expand=1,
                                    scroll=ft.ScrollMode.ALWAYS,
                                    controls=[
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.Image(
                                                    expand=1, src=METHOD_IMAGE_PATH
                                                )
                                            ],
                                        ),
                                        ft.Text(METHOD_EXPLANATION),
                                        ft.Divider(height=1, color=ft.colors.WHITE),
                                        ft.Text("Step 1. Run"),
                                        ft.Row(
                                            [
                                                ft.TextButton(
                                                    text="RUN",
                                                    expand=1,
                                                    on_click=self.click_run,
                                                )
                                            ]
                                        ),
                                    ],
                                ),
                                ft.Divider(height=1, color=ft.colors.WHITE),
                                ft.Row(
                                    controls=[
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.START,
                                            expand=1,
                                            controls=[
                                                ft.TextButton(
                                                    "<- Back",
                                                    on_click=self.to_previous_tab,
                                                )
                                            ],
                                        ),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.END,
                                            expand=1,
                                            controls=[
                                                ft.TextButton(
                                                    "Next ->",
                                                    on_click=self.to_next_tab,
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    def reload(self):
        self.leaf_img.set_image(self.data.extract_leaf_img_base64, "base64")
        self.fvfm_img.set_image(self.data.extract_fvfm_img_base64, "base64")
        self.page.update()

    def click_run(self, e):
        pass
