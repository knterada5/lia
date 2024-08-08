import flet as ft


class BoxIntSlider(ft.Row):
    """Textbox and slider with synchronized values."""

    def __init__(self, value, max, min, divisions=None):
        super().__init__()
        if divisions is None:
            divisions = max
        input_filter = ft.InputFilter("^[0-9]*")
        text_width = 20 * len(str(max))
        self.text = ft.TextField(
            width=text_width,
            value=value,
            input_filter=input_filter,
            on_change=self.update_slider_value,
            on_submit=self.submit,
            border=ft.InputBorder.OUTLINE,
        )
        self.slider = ft.Slider(
            value=value,
            min=min,
            max=max,
            divisions=divisions,
            label="{value}",
            expand=1,
            on_change=self.update_text_value,
        )
        self.controls = [self.slider, self.text]

    def update_text_value(self, e):
        """Update text value when slider value changed."""
        self.text.value = f"{int(e.control.value)}"
        self.page.update()

    def update_slider_value(self, e):
        """Update slider value when text value changed."""
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
        """Set value to slider when text submitted."""
        value = e.control.value
        if value == "":
            self.text.value = self.slider.min
        elif int(value) > self.slider.max:
            self.text.value = self.slider.max
        elif int(value) < self.slider.min:
            self.text.value = self.slider.min
        self.page.update()

    def get_value(self):
        """Get value."""
        return int(self.text.value)

    def set_value(self, value):
        """Set value to textbox and slider."""
        self.text.value = value
        self.slider.value = value
        self.page.update()
