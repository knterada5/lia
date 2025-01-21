import cv2
import flet as ft
import numpy as np

from lia.basic.thread import WorkingThread
from lia.basic.transform.image import to_base64
from lia.data.color_fvfm import ColorFvFmData
from lia.gui.base.run_tab import RunTab
from lia.gui.widgets.image_container import ImageContainer
from lia.gui.widgets.range_slider import BoxIntRangeSlider

SELECT_COLOR_TAB = "Select Color"
DEFAULT_IMAGE_PATH = "/images/photo.png"
ARROW_IMAGE_PATH = "/images/arrow.png"
DEFAULT_HSV_1 = [[0, 0, 0], [30, 255, 255]]
DEFAULT_HSV_2 = [[30, 0, 0], [60, 255, 255]]


class SelectColorTab(RunTab):
    def __init__(self, data: ColorFvFmData):
        super().__init__()
        self.data: ColorFvFmData = data
        self.text = SELECT_COLOR_TAB
        self.set_contents()

    def set_contents(self):
        self.leaf_image = ImageContainer(DEFAULT_IMAGE_PATH)
        self.color1_leaf_image = ImageContainer(DEFAULT_IMAGE_PATH)
        self.color2_leaf_image = ImageContainer(DEFAULT_IMAGE_PATH)
        self.color1_image = ImageContainer(DEFAULT_IMAGE_PATH)
        self.color2_image = ImageContainer(DEFAULT_IMAGE_PATH)

        self.hue1_slider = BoxIntRangeSlider(
            DEFAULT_HSV_1[0][0], DEFAULT_HSV_1[1][0], 180, 0
        )
        self.hue2_slider = BoxIntRangeSlider(
            DEFAULT_HSV_2[0][0], DEFAULT_HSV_2[1][0], 180, 0
        )
        self.saturation1_slider = BoxIntRangeSlider(
            DEFAULT_HSV_1[0][1], DEFAULT_HSV_1[1][1], 255, 0
        )
        self.saturation2_slider = BoxIntRangeSlider(
            DEFAULT_HSV_2[0][1], DEFAULT_HSV_2[1][1], 255, 0
        )
        self.value1_slider = BoxIntRangeSlider(
            DEFAULT_HSV_1[0][2], DEFAULT_HSV_1[1][2], 255, 0
        )
        self.value2_slider = BoxIntRangeSlider(
            DEFAULT_HSV_2[0][2], DEFAULT_HSV_2[1][2], 255, 0
        )

        # Layout
        self.content = ft.Container(
            padding=ft.padding.all(10),
            content=ft.Row(
                expand=True,
                controls=[
                    ft.Container(  # Image area
                        border=ft.border.all(2, ft.colors.WHITE),
                        expand=2,
                        padding=ft.padding.all(10),
                        content=ft.Column(
                            controls=[
                                ft.Container(expand=5, content=self.leaf_image),
                                ft.Image(expand=1, src=ARROW_IMAGE_PATH),
                                ft.Container(
                                    expand=5,
                                    content=ft.Row(
                                        controls=[
                                            self.color1_leaf_image,
                                            self.color2_leaf_image,
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    ft.Container(  # Method area
                        border=ft.border.all(2, ft.colors.WHITE),
                        padding=ft.padding.all(10),
                        expand=1,
                        content=ft.Column(
                            expand=1,
                            controls=[
                                ft.Column(
                                    expand=1,
                                    scroll=ft.ScrollMode.ALWAYS,
                                    controls=[
                                        ft.Text(value="Color1"),
                                        ft.Container(
                                            height=80, content=self.color1_image
                                        ),
                                        self.hue1_slider,
                                        self.saturation1_slider,
                                        self.value1_slider,
                                        ft.Text(value="Color 2"),
                                        ft.Container(content=self.color2_image),
                                        self.hue2_slider,
                                        self.saturation2_slider,
                                        self.value2_slider,
                                    ],
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )
        self.update_color_range_image(
            DEFAULT_HSV_1[0][0],
            DEFAULT_HSV_1[0][1],
            DEFAULT_HSV_1[0][2],
            DEFAULT_HSV_1[1][0],
            DEFAULT_HSV_1[1][1],
            DEFAULT_HSV_1[1][2],
            self.color1_image,
        )
        self.update_color_range_image(
            DEFAULT_HSV_2[0][0],
            DEFAULT_HSV_2[0][1],
            DEFAULT_HSV_2[0][2],
            DEFAULT_HSV_2[1][0],
            DEFAULT_HSV_2[1][1],
            DEFAULT_HSV_2[1][2],
            self.color2_image,
        )

    def reload(self):
        self.leaf_image.set_image(self.data.align_leaf_img_base64, "base64")
        # self.update_color_range_image(
        #     DEFAULT_HSV_1[0][0],
        #     DEFAULT_HSV_1[0][1],
        #     DEFAULT_HSV_1[0][2],
        #     DEFAULT_HSV_1[1][0],
        #     DEFAULT_HSV_1[1][1],
        #     DEFAULT_HSV_1[1][2],
        #     self.color1_image,
        # )
        # self.update_color_range_image(
        #     DEFAULT_HSV_2[0][0],
        #     DEFAULT_HSV_2[0][1],
        #     DEFAULT_HSV_2[0][2],
        #     DEFAULT_HSV_2[1][0],
        #     DEFAULT_HSV_2[1][1],
        #     DEFAULT_HSV_2[1][2],
        #     self.color2_image,
        # )
        self.page.update()

    def click_run(self, e):
        if self.data.align_leaf_img is None:
            self.show_error_dialog(
                "Aligned image not found.\nRun the previous tabs before selecting color."
            )
            return
        self.thread = WorkingThread(target=self.run)
        self.thread.start()

    def run(self):
        pass

    def change(self):
        pass

    def update_color_range_image(
        self,
        hue_low,
        saturation_low,
        value_low,
        hue_high,
        saturation_high,
        value_high,
        color_image: ImageContainer,
    ):
        height = 40
        width = 400
        # height = int(self.color1_image.height)
        # width = int(self.color1_image.width)
        if width == 0:
            width = 1
        if height == 0:
            height = 1
        hue = np.linspace(hue_low, hue_high, width)
        saturation = np.linspace(saturation_low, saturation_high, height)
        value = np.linspace(value_low, value_high, height)
        image_hsv = np.array(
            [[h, s, v] for (s, v) in zip(saturation, value) for h in hue], np.uint8
        ).reshape(height, width, 3)
        image_bgr = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)
        image_base64 = to_base64(image_bgr)
        color_image.set_image(image_base64, "base64")
