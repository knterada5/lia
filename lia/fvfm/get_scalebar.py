"""Get Fv/Fm scale bar area."""

import cv2

from lia.basic.get.contours import get_cnts
from lia.basic.get.image import WHITE_INV_THRESH, get_white_bg_binary_img

BAR_AREA_RATIO = 100


def get_bar_area(img, white_inv_thresh=WHITE_INV_THRESH, bar_area_ratio=BAR_AREA_RATIO):
    """Get Fv/Fm scale bar.

    Parameters
    ----------
    img : numpy.ndarray
        Input image.
    white_inv_thresh : int, optional
        Threshold of white background.
    bar_area_ratio : int, optional
        Ratio of minimum bar size.

    Returns
    -------
    bar_area : [int, int, int, int]
        Bar area rectangle.

    Raises
    ------
    ValueError
        Cannot find scale bar.
    """
    binary_img = get_white_bg_binary_img(img, white_inv_thresh)
    cnts = get_cnts(binary_img, bar_area_ratio)
    img_height = img.shape[0]
    for cnt in cnts:
        x, y, width, height = cv2.boundingRect(cnt)
        ratio = height / width
        occupancy = height / img_height
        if (ratio > 0.7) and (occupancy > 0.8):
            return [x, y, width, height]
    raise ValueError("Cannot find scalebar.")
