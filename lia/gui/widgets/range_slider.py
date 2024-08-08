import flet as ft


class BoxIntRangeSlider(ft.Row):
    """Textboxes and Range slider with synchronized values.

    Parameters
    ----------
    start_value : int
        THe smaller default value.
    end_value : int
        The larger default value.
    max : int
        Maximum value of selection.
    min : int
        Minimum value of selection.
    devisions : int
        The number of discrete divisions.
    """

    def __init__(self, start_value, end_value, max, min, divisions=None):
        super().__init__()
        if divisions is None:
            divisions = max
        input_filter = ft.InputFilter("^[0-9]*")
        text_width = 20 * len(str(max))
        self.text1 = ft.TextField(
            width=text_width,
            value=start_value,
            input_filter=input_filter,
            on_change=self.update_slider_start,
            on_submit=self.submit_text1,
            border=ft.InputBorder.OUTLINE,
        )
        self.text2 = ft.TextField(
            width=text_width,
            value=end_value,
            input_filter=input_filter,
            on_change=self.update_slider_end,
            on_submit=self.submit_text2,
            border=ft.InputBorder.OUTLINE,
        )
        self.slider = ft.RangeSlider(
            start_value=start_value,
            end_value=end_value,
            max=max,
            min=min,
            divisions=divisions,
            label="{value}",
            expand=1,
            on_change=self.update_text_value,
        )
        self.controls = [self.text1, self.slider, self.text2]

    def update_text_value(self, e: ft.ControlEvent):
        """Update textbox values when slider value changed."""
        self.text1.value = f"{int(e.control.start_value)}"
        self.text2.value = f"{int(e.control.end_value)}"
        self.page.update()

    def update_slider_start(self, e):
        """Update smaller value of slider when text value changed."""
        value = e.control.value
        if value == "":
            value = 0
        elif int(value) > self.slider.max:
            value = self.slider.max
        elif int(value) < self.slider.min:
            value = self.slider.min
        self.slider.start_value = int(value)
        self.page.update()

    def update_slider_end(self, e):
        """Update larger value of slider when text value changed."""
        value = e.control.value
        if value == "":
            value = 0
        elif int(value) > self.slider.max:
            value = self.slider.max
        elif int(value) < self.slider.min:
            value = self.slider.min
        self.slider.end_value = int(value)
        self.page.update()

    def submit_text1(self, e):
        """Set value to slider when smaller value submitted."""
        value = e.control.value
        if value == "":
            self.text1.value = self.slider.min
        elif int(value) > self.slider.max:
            self.text1.value = self.slider.max
        elif int(value) < self.slider.min:
            self.text1.value = self.slider.min
        self.page.update()

    def submit_text2(self, e):
        """Set value to slider when larger value submitted."""
        value = e.control.value
        if value == "":
            self.text2.value = self.slider.min
        elif int(value) > self.slider.max:
            self.text2.value = self.slider.max
        elif int(value) < self.slider.min:
            self.text2.value = self.slider.min
        self.page.update()

    def get_value(self):
        """Get values."""
        return int(self.text1.value), int(self.text2.value)

    def set_value(self, start_value, end_value):
        """Set values to textboxes and slider."""
        self.slider.start_value = start_value
        self.slider.end_value = end_value
        self.text1.value = start_value
        self.text2.value = end_value
        self.page.update()
