"""Get Fv/Fm value list."""

from .calculate_ratio import calculate_ratio
from .get_scalebar import BAR_AREA_RATIO, WHITE_INV_THRESH, get_bar_area
from .read_scalebar import read_fvfm_value


def get_fvfm_list(
    img, white_inv_thresh=WHITE_INV_THRESH, bar_area_ratio=BAR_AREA_RATIO
):
    """Get list of color and Fv/Fm value.

    Parameters
    ----------
    img : numpy.ndarray
        Input image.

    Returns
    -------
    fvfm_color_list : [[int, int, int], ...]
        List of Fv/Fm scale color.
    fvfm_value_lsit : [int, ...]
        List of Fv/Fm scale value.

    Raises
    ------
    ValueError
        Cannot get Fv/Fm value.
    """
    bar_area = get_bar_area(img, white_inv_thresh, bar_area_ratio)
    top = bar_area[1]
    bottom = bar_area[1] + bar_area[3]
    center_x = int(bar_area[0] + (bar_area[2] / 2))
    fvfm_value_list = read_fvfm_value(img)
    std_fvfm_pos_y = fvfm_value_list[0][0]
    std_fvfm_val = int(fvfm_value_list[0][1] * 1000)
    scale_fvfm_list = [[x[0], int(x[1] * 1000)] for x in fvfm_value_list]
    scale = calculate_ratio(scale_fvfm_list)
    upper_num = int((std_fvfm_pos_y - top) / scale)
    lower_num = int((bottom - std_fvfm_pos_y) / scale)
    fvfm_list = []
    for i in range(1, upper_num + 1):
        fvfm_value = std_fvfm_val + i
        pos_y = int(std_fvfm_pos_y - (i * scale))
        color = img[pos_y, center_x].tolist()
        fvfm_list.append([color, fvfm_value / 1000])
    for i in range(1, lower_num + 1):
        fvfm_value = std_fvfm_val - i
        pos_y = int(std_fvfm_pos_y + (i * scale))
        color = img[pos_y, center_x].tolist()
        fvfm_list.append([color, fvfm_value / 1000])
    if len(fvfm_list) > 0:
        fvfm_list.sort(key=lambda x: x[1], reverse=True)
        fvfm_color_list = [x[0] for x in fvfm_list]
        fvfm_value_list = [x[1] for x in fvfm_list]
        return fvfm_color_list, fvfm_value_list
    else:
        raise ValueError("Cannot get Fv/Fm value.")
