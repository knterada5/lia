import flet as ft


class BoxSlider(ft.Row):
    def __init__(self, value, max, min, divisions=None):
        super().__init__()
        if divisions is None:
            divisions = max
        _filter = ft.InputFilter("^[0-9]*")
        text_width = 20 * len(str(max))
        self.text = ft.TextField(
            width=text_width,
            value=value,
            input_filter=_filter,
            on_change=self.update_text,
            on_submit=self.submit,
        )
        self.slider = ft.Slider(
            value=value,
            min=min,
            max=max,
            divisions=divisions,
            label="{value}",
            expand=1,
            on_change=self.update_slider,
        )
        self.controls = [self.slider, self.text]

    def update_slider(self, e):
        self.text.value = f"{int(e.control.value)}"
        self.page.update()

    def update_text(self, e):
        value = e.control.value
        if value == "":
            value = 0
        elif int(value) > self.slider.max:
            value = self.slider.max
        elif int(value) < self.slider.min:
            value = self.slider.min
        self.slider.value = int(value)
        self.page.update()

    def submit(self, e):
        value = e.control.value
        if value == "":
            self.text.value = 0
        elif int(value) > self.slider.max:
            self.text.value = self.slider.max
        elif int(value) < self.slider.min:
            self.text.value = self.slider.min
        self.page.update()

    def get_value(self):
        return int(self.text.value)

    def set_value(self, value):
        self.text.value = value
        self.slider.value = value
        self.page.update()
