import cv2
import flet as ft

from lia import AlignLeaf
from lia.basic.thread import WorkingThread
from lia.basic.transform.image import to_base64
from lia.data.color_fvfm import ColorFvFmData
from lia.gui.base.run_tab import RunTab
from lia.gui.widgets.image_container import ImageContainer

ALIGN_TITLE = "Align"
DEFAULT_IMAGE_PATH = "/images/photo.png"
METHOD_EXPLANATION = "Adjust the size and tilt so that the two images overlap exactly."
RIGHT_ARROW = "/images/arrow_right.png"


class AlignTab(RunTab):
    """ColorFvFm application tab: Align leaves."""

    def __init__(self, data: ColorFvFmData):
        super().__init__()
        self.data: ColorFvFmData = data
        self.text = ALIGN_TITLE
        self.align = AlignLeaf()
        self.set_contents()

    def set_contents(self):
        """Set controls."""
        self.leaf_img = ImageContainer(DEFAULT_IMAGE_PATH)
        self.fvfm_img = ImageContainer(DEFAULT_IMAGE_PATH)
        self.aligned_leaf_img = ImageContainer(DEFAULT_IMAGE_PATH)
        self.aligned_fvfm_img = ImageContainer(DEFAULT_IMAGE_PATH)
        self.overlay_img = ImageContainer(DEFAULT_IMAGE_PATH)

        # Layout
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
                                    expand=1,
                                    controls=[
                                        ft.Container(expand=6, content=self.leaf_img),
                                        ft.Image(expand=1, src=RIGHT_ARROW),
                                        ft.Container(
                                            expand=6, content=self.aligned_leaf_img
                                        ),
                                    ],
                                ),
                                ft.Row(
                                    expand=1,
                                    controls=[
                                        ft.Container(expand=6, content=self.fvfm_img),
                                        ft.Image(expand=1, src=RIGHT_ARROW),
                                        ft.Container(
                                            expand=6, content=self.aligned_fvfm_img
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    ft.Column(
                        expand=1,
                        controls=[
                            ft.Container(
                                expand=1,
                                border=ft.border.all(2, ft.colors.WHITE),
                                padding=ft.padding.only(
                                    left=10, top=10, right=10, bottom=10
                                ),
                                content=ft.Column(
                                    expand=1,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            text_align=ft.TextAlign.CENTER,
                                            value="Overlay image",
                                        ),
                                        self.overlay_img,
                                    ],
                                ),
                            ),
                            ft.Container(
                                expand=1,
                                padding=ft.padding.only(
                                    left=10, top=10, right=10, bottom=10
                                ),
                                border=ft.border.all(2, ft.colors.WHITE),
                                content=ft.Column(
                                    expand=1,
                                    controls=[
                                        ft.Column(
                                            expand=1,
                                            scroll=ft.ScrollMode.ALWAYS,
                                            controls=[
                                                ft.Text(METHOD_EXPLANATION),
                                                ft.Divider(
                                                    height=1, color=ft.colors.WHITE
                                                ),
                                                ft.Text("Step 1. Run"),
                                                ft.Row(
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    controls=[
                                                        ft.OutlinedButton(
                                                            text="RUN",
                                                            expand=1,
                                                            expand_loose=True,
                                                            on_click=self.click_run,
                                                        )
                                                    ],
                                                ),
                                            ],
                                        ),
                                        ft.Divider(height=1, color=ft.colors.WHITE),
                                        ft.Row(
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
                ],
            ),
        )

    def reload(self):
        """Reload image, when tab changed."""
        self.leaf_img.set_image(self.data.extract_leaf_img_base64, "base64")
        self.fvfm_img.set_image(self.data.extract_fvfm_img_base64, "base64")
        self.page.update()

    def click_run(self, e):
        """Running process."""
        leaf_img = self.data.extract_leaf_img
        fvfm_img = self.data.extract_fvfm_img
        if leaf_img is None and fvfm_img is None:
            self.show_error_dialog(
                'Extracted leaf images not found.\nGo back to the "Extract Leaf" and "Get Fv/Fm value" tab to extract leaves.'
            )
            return
        elif leaf_img is None:
            self.show_error_dialog(
                'Extracted leaf image not found.\nGo back to the "Extract Leaf" tab to extract leaf.'
            )
            return
        elif fvfm_img is None:
            self.show_error_dialog(
                'Extracted Fv/Fm leaf image not found.\nGo back to the "Get Fv/Fm value" tab to extract leaf.'
            )
            return
        self.thread = WorkingThread(target=self.run)
        self.thread.start()

    def run(self):
        """Run Align leaves."""
        self.show_progress_dialog("Align leaves", "Running...")
        try:
            self.data.align_fvfm_img, self.data.align_leaf_img = self.align.horizontal(
                self.data.extract_fvfm_img,
                self.data.extract_leaf_img,
                self.data.fvfm_cnts,
                self.data.leaf_cnts,
            )
            self.data.align_fvfm_img_base64 = to_base64(self.data.align_fvfm_img)
            self.data.align_leaf_img_base64 = to_base64(self.data.align_leaf_img)
            self.aligned_fvfm_img.set_image(self.data.align_fvfm_img_base64, "base64")
            self.aligned_leaf_img.set_image(self.data.align_leaf_img_base64, "base64")
            img_overlay = cv2.addWeighted(
                src1=self.data.align_leaf_img,
                src2=self.data.align_fvfm_img,
                alpha=1,
                beta=0.3,
                gamma=0,
            )
            img_overlay_base64 = to_base64(img_overlay)
            self.overlay_img.set_image(img_overlay_base64, "base64")
            self.page.update()
            self.page.close(self.dialog)
        except Exception as e:
            self.page.close(self.dialog)
            self.show_error_dialog(str(e))
