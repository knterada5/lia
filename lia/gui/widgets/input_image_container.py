import flet as ft

from lia.data.color_fvfm import ColorFvFmData


class InputImage(ft.Column):
    def __init__(self, input_func, **kwargs):
        super().__init__(kwargs)
        self.input_func = input_func
        self.set_content()

    def set_content(self):
        self.text = ft.Text("Input image path.", expand=1, no_wrap=True)
        self.img = ft.Image(src="src/photo.png", expand=1)
        self.expand = True
        self.alignment = ft.alignment.center
        self.controls = [
            ft.Container(
                content=ft.Row(
                    [
                        self.text,
                        ft.TextButton(
                            "Select Image",
                            icon=ft.icons.INSERT_PHOTO_OUTLINED,
                            on_click=self.select_image,
                        ),
                    ],
                    expand=1,
                ),
                border=ft.border.only(bottom=ft.border.BorderSide(5, ft.colors.PINK)),
                expand=1,
            ),
            ft.Container(
                content=ft.Row([self.img], alignment=ft.alignment.center, expand=True),
                expand=5,
            ),
        ]

    def select_image(self, e):
        file_picker = ft.FilePicker(on_result=self.input_filepicker)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files()

    def input_filepicker(self, e: ft.FilePickerResultEvent):
        if e.files is None:
            return
        input_path = e.files[0].path
        self.input_func(input_path)
        self.set_image(input_path)
        self.page.update()

    def set_image(self, input_path):
        if input_path is None:
            return
        self.text.value = input_path
        self.img.src = input_path
