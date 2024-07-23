"""Get image."""

import re

import cv2

LEAF_COLOR_FORMAT = "HSV"
LEAF_COLOR_LOWER = (30, 50, 50)
LEAF_COLOR_UPPER = (90, 255, 200)


def get_image_in_color_range(
    img, lower=LEAF_COLOR_LOWER, upper=LEAF_COLOR_UPPER, color_format=LEAF_COLOR_FORMAT
):
    """Get mask in color range.

    Parameters
    ----------
    img : numpy.ndarray
        Input image.
    lower : (int, int, int)
        Lower color.
    upper : (int, int, int)
        Upper color value.
    color_format : str
        "HSV" or "RGB".

    Returns
    -------
    mask : numpy.ndarray
        Mask.

    Raises
    ------
    ValueError
        Invalid color format.
    """
    if color_format.lower() == "hsv":
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv, lower, upper)
    elif re.match("bgr|rgb", color_format.lower()):
        mask = cv2.inRange(img, lower, upper)
    else:
        raise ValueError(
            f'Invalid color format: {color_format}\nPlease select "RGB" or "HSV".'
        )
    return mask
