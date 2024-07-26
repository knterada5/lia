import dataclasses

import numpy as np


@dataclasses.dataclass
class ColorFvFmData:
    input_leaf_path: str = None
    input_fvfm_path: str = None
    input_leaf_img: np.ndarray = None
    input_fvfm_img: np.ndarray = None
    extract_leaf_img: np.ndarray = None
    extract_fvfm_img: np.ndarray = None
    extract_leaf_img_base64: str = None
    extract_fvfm_img_base64: str = None
    leaf_cnts: np.ndarray = None
    fvfm_cnts: np.ndarray = None
    fvfm_color_list: list = None
    fvfm_value_list: list = None
    align_leaf_img: np.ndarray = None
    align_fvfm_img: np.ndarray = None
    align_leaf_img_base64: str = None
    align_fvfm_img_base64: str = None
