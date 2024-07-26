"""Extract contours of leaf from an image."""

import cv2
import numpy as np

from lia.extract.leaf import (
    BEYOND_ERROR_ELLIPSE,
    BLANK_RATIO,
    CANNY_THRESH1,
    CANNY_THRESH2,
    DIFF_ELLIPSE_SIZE,
    LEAF_COLOR_FORMAT,
    LEAF_COLOR_LOWER,
    LEAF_COLOR_UPPER,
    MIN_CNTS_RATIO,
    NOISE_THRESH,
    NUM_NOISE_THRESH,
    THRESH,
    WHITE_BG_THRESH,
    extract_leaf_by_color,
    extract_leaf_by_thresh,
)

from .base import ImageCore


class ExtractLeaf(ImageCore):
    """Extract leaf contours from image.

    Attributes
    ----------
    min_cnts_ratio : int
        Minimum area ratio to be detected (min_area = area / min_cnts_ratio).
    diff_ellipse_size : int
        Tolerance for difference between approximate ellipse and contour.
    beyond_error_ellipse : int
        Percentage of approximate ellipses that extend beyond the image.
    thresh : int
        Threshold to detect contours.
    blank_ratio : int
        Max ratio of blank area.
    noise_ratio_thresh : int
        Threshold of noise contours.
    canny_thresh1 : int
        Threshold 1 for canny.
    canny_thresh2 : int
        Threshold 2 for canny.
    noise_thresh : int
        Threshold for contours of noise.
    leaf_color_format : str
        Color format, HSV or RGB.
    leaf_color_lower : (int, int, int)
        Lower of color range.
    leaf_color_upper : (int, int, int)
        Upper of color range.
    white_bg_thresh : int
        Threshold of binarization for white background.
    """

    def __init__(self):
        super().__init__()
        # Set default value.
        self.min_cnts_ratio = MIN_CNTS_RATIO
        self.diff_ellipse_size = DIFF_ELLIPSE_SIZE
        self.beyond_error_ellipse = BEYOND_ERROR_ELLIPSE
        self.thresh = THRESH
        self.blank_ratio = BLANK_RATIO
        self.noise_ratio_thresh = NUM_NOISE_THRESH
        self.canny_thresh1 = CANNY_THRESH1
        self.canny_thresh2 = CANNY_THRESH2
        self.noise_thresh = NOISE_THRESH
        self.leaf_color_format = LEAF_COLOR_FORMAT
        self.leaf_color_lower = LEAF_COLOR_LOWER
        self.leaf_color_upper = LEAF_COLOR_UPPER
        self.white_bg_thresh = WHITE_BG_THRESH

    def __draw_cnts_area(self, img, cnt):
        """Draw contours.

        Parameters
        ----------
        img : numpy.ndarray
            Input color image.
        cnts : [[[int, int]], ...]
            List of contours.

        Returns
        -------
        [numpy.ndarray]
            Images with contours drawn.
        """
        mask = np.zeros(img.shape, np.uint8)
        cv2.drawContours(mask, [cnt], -1, (255, 255, 255), -1)
        res_img = cv2.bitwise_and(img, mask)
        return res_img

    def get_by_thresh(self, input):
        """Extract leaf by detecting contours.

        Parameters
        ----------
        input : str or numpy.ndarray
            Input image path or image in ndarray format.

        Returns
        -------
        leaf_cnt_imgs : [numpy.ndarray, ...]
            List of images depicting the detected leaf contour candidates.
        leaf_cnt_candidates : [(array[[[int, int]], ...], ...), ...]
            Contours list of leaf candidates.
        """
        img = self.input_img(input)
        leaf_cnt_candidates = extract_leaf_by_thresh(
            img,
            self.thresh,
            self.blank_ratio,
            self.noise_ratio_thresh,
            self.min_cnts_ratio,
            self.canny_thresh1,
            self.canny_thresh2,
            self.noise_ratio_thresh,
            self.diff_ellipse_size,
            self.beyond_error_ellipse,
            self.white_bg_thresh,
        )
        leaf_cnt_imgs = []
        for cnt in leaf_cnt_candidates:
            leaf_img = self.__draw_cnts_area(img, cnt)
            leaf_cnt_imgs.append(leaf_img)
        return leaf_cnt_imgs, leaf_cnt_candidates

    def get_by_color(self, input):
        """Extract leaf by color range.

        Parameters
        ----------
        input : str or numpy.ndarray
            Input image path or image in ndarray format.

        Returns
        -------
        leaf_cnt_img : numpy.ndarray
            Image of a leaf outline drawn.
        leaf_cnt : (array[[[int, int]],...])
            Leaf contours.
        """
        img = self.input_img(input)
        leaf_cnt = extract_leaf_by_color(
            img,
            self.leaf_color_lower,
            self.leaf_color_upper,
            self.leaf_color_format,
            self.min_cnts_ratio,
        )
        leaf_cnt_img = self.__draw_cnts_area(img, leaf_cnt)
        return leaf_cnt_img, leaf_cnt

    def set_param(self, **kwargs):
        """Set parameter.

        Parameters
        ----------
        min_cnts_ratio : int
            Minimum area ratio (min_area = area / min_ratio).
        diff_ellipse_size : int
            Tolerance for difference between approximate ellipse and contour.
        beyond_error_ellipse : int
            Percentage of approximate ellipses that extend beyond the image.
        thresh : int
            Threshold to detect contours.
        blank_ratio : int
            Max ratio of blank area.
        noise_ratio_thresh : int
            Threshold of noise contours.
        canny_thresh1 : int
            Threshold 1 for canny.
        canny_thresh2 : int
            Threshold 2 for canny.
        noise_thresh : int
            Threshold for contours of noise.
        leaf_color_format : str
            Color format, HSV or RGB.
        leaf_color_lower : (int, int, int)
            Lower of color range.
        leaf_color_upper : (int, int, int)
            Upper of color range.
        white_bg_thresh : int
            Threshold of binarization for white background.
        """
        super().set_param(**kwargs)
