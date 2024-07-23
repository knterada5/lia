"""Get Fv/Fm values and their colors."""

from lia.fvfm.get_value_list import BAR_AREA_RATIO, WHITE_INV_THRESH, get_fvfm_list

from .base import ImageCore


class GetFvFm(ImageCore):
    """Calculate Fv/Fm values and their colors from the scale bar.

    Attributes
    ----------
    white_inv_thresh : int
        Threshold of whtie background.
    bar_area_ratio : int
        Ratio of minimum bar size.
    """

    def __init__(self) -> None:
        self.white_inv_thresh = WHITE_INV_THRESH
        self.bar_area_ratio = BAR_AREA_RATIO

    def get_list(self, input_path):
        """Get list of Fv/Fm value and color.

        Parameters
        ----------
        input_path : str or numpy.ndarray
            Input image or its path.

        Returns
        -------
        fvfm_color_list : [[[int, int, int], ...]
            List of Fv/Fm scale color.
        fvfm_value_list : [int, ...]
            List of Fv/Fm scale value.
        """
        img = self.input_img(input_path)
        fvfm_color_list, fvfm_value_list = get_fvfm_list(
            img, self.white_inv_thresh, self.bar_area_ratio
        )
        return fvfm_color_list, fvfm_value_list

    def set_param(self, **kwargs):
        """Set parameter.

        Parameters
        ----------
        white_inv_thresh : int
            Threshold of whtie background.
        bar_area_ratio : int
            Ratio of minimum bar size.
        """
        super().set_param(**kwargs)
