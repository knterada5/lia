"""Get contours."""

from multiprocessing import Pool

import cv2
import numpy as np

from lia.basic.evaluate.noise import (
    CANNY_THRESH1,
    CANNY_THRESH2,
    NOISE_THRESH,
    get_noise,
)

from ._consts import MIN_CNTS_RATIO

THRESH = 60
BLANK_RATIO = 98
NUM_NOISE_THRESH = 50
WHITE_BG_THRESH = 30


def get_cnts(img, min_cnts_ratio=MIN_CNTS_RATIO):
    """Get contours list from binary image.

    Parameters
    ----------
    img : numpy.ndarray
        Input binary image.
    min_ratio : int
        Minimum area ratio (min_area = area / min_ratio).

    Returns
    -------
    cnts_list : list
        List of contours.
    """
    height, width = img.shape[:2]
    min_area = (height * width) / min_cnts_ratio
    cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_list = list(filter(lambda x: cv2.contourArea(x) > min_area, cnts))
    return cnts_list


def get_cnts_from_hsv(
    img,
    thresh=THRESH,
    blank_ratio=BLANK_RATIO,
    noise_ratio_thresh=NUM_NOISE_THRESH,
    min_cnts_ratio=MIN_CNTS_RATIO,
    canny_thresh1=CANNY_THRESH1,
    canny_thresh2=CANNY_THRESH2,
    noise_thresh=NOISE_THRESH,
):
    """Sort H, S, and V in order of clarity of leaf outline.

    Parameters
    ----------
    img : numpy.ndarray
        Input BGR image
    thresh : int
        Minimum threshold
    noise_ratio : int (default: 98)
        Max percentage of screen occupied by noise.

    Returns
    -------
    sorted_cnts_list : list
        lList of contours of H, S, and V in order of decreasing noise.

    Raises
    ------
    ValueError
        If no contours were detected.
    """
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = cv2.split(img_hsv)
    image_list = []
    for image in hsv:
        image_list.append(
            [
                image,
                thresh,
                blank_ratio,
                min_cnts_ratio,
                canny_thresh1,
                canny_thresh2,
                noise_thresh,
                noise_ratio_thresh,
            ]
        )
    with Pool(3) as p:
        evaluated = p.map(pool_evaluate_clarity, image_list)
    noise_list = list(filter(lambda x: x[0] is not None, evaluated))
    if noise_list is not None:
        noise_list.sort(key=lambda x: x[0])
        sorted_cnts_list = [r[1] for r in noise_list]
        return sorted_cnts_list
    else:
        raise ValueError("No contours were detected.")


def pool_evaluate_clarity(args):
    """Pool function; Evaluate clarity.

    Parameters
    ----------
    image : numpy.ndarray
        Input image.
    thresh : int, optional
        Threshold for binarization.
    blank_ratio : int, optional
        Ratio of blank.
    min_cnts_ratio : int, optional
        Minimum area ratio to detect contours.
    canny_thresh1 : int, optional
        Canny threshold 1.
    canny_thresh2 : int, optional
        Canny threshold 2.
    noise_thresh : int, optional
        Threshold of noise.
    num_noise_thresh : int, optional
        THreshold for number of noise.

    Returns
    -------
    num_noise : int
        Number of noise.
    cnts_list : list
        List of contours.
    """
    num_noise, cnts_list = evaluate_clarity(*args)
    return num_noise, cnts_list


def evaluate_clarity(
    image,
    thresh=THRESH,
    blank_ratio=BLANK_RATIO,
    min_cnts_ratio=MIN_CNTS_RATIO,
    canny_thresh1=CANNY_THRESH1,
    canny_thresh2=CANNY_THRESH2,
    noise_thresh=NOISE_THRESH,
    num_noise_thresh=NUM_NOISE_THRESH,
):
    """Evalutate clarity.

    Parameters
    ----------
    image : numpy.ndarray
        Input image.
    thresh : int, optional
        Threshold for binarization.
    blank_ratio : int, optional
        Ratio of blank.
    min_cnts_ratio : int, optional
        Minimum area ratio to detect contours.
    canny_thresh1 : int, optional
        Canny threshold 1.
    canny_thresh2 : int, optional
        Canny threshold 2.
    noise_thresh : int, optional
        Threshold of noise.
    num_noise_thresh : int, optional
        THreshold for number of noise.

    Returns
    -------
    num_noise : int
        Number of noise.
    cnts_list : list
        List of contours.
    """
    height, width = image.shape[:2]
    area = height * width
    _, img_bin = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)
    white = int(np.sum(img_bin) / 255)
    black = area - white
    if ((white / area) * 100 > blank_ratio) or ((black / area) * 100 > blank_ratio):
        return None, None
    cnts_list = get_cnts(img_bin, min_cnts_ratio)
    if len(cnts_list) == 0:
        return None, None
    num_noise, noise_ratio = get_noise(
        image, canny_thresh1, canny_thresh2, noise_thresh
    )
    if noise_ratio > num_noise_thresh:
        return None, None
    return num_noise, cnts_list


def get_cnts_white_background(
    img, white_bg_thresh=WHITE_BG_THRESH, min_cnts_ratio=MIN_CNTS_RATIO
):
    """Get contours list from white background image.

    Parameters
    ----------
    img : numpy.ndarray
        Input color image.
    white_bg_thresh : int
        Threshold of binarization for white background.
    min_cnts_ratio : int
        Minimum area ratio (min_area = area / min_ratio).

    Returns
    -------
    cnts_list : [(array[[[int, int]], ...], ...), ...]
        List of contours.
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray_inv = cv2.bitwise_not(img_gray)
    _, bin = cv2.threshold(img_gray_inv, white_bg_thresh, 255, cv2.THRESH_BINARY)
    cnts_list = get_cnts(bin, min_cnts_ratio)
    return cnts_list
