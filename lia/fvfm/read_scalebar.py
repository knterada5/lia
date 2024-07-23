"""Read Fv/Fm value from scalebar."""

import re


def read_fvfm_value(img):
    """Read Fv/Fm value from image.

    Parameters
    ----------
    img : numpy.ndarray
        Input image.

    Returns
    -------
    fvfm_value_list : [[float, int], ...]
        List of position height and Fv/Fm value.

    Raises
    ------
    ValueError
        If less than 2 value.
    """
    import easyocr

    reader = easyocr.Reader(["en"])
    text = reader.readtext(img)
    fvfm_value_list = []
    for word in text:
        if re.compile("0(\.|,)\d{2}$").match(word[1]):
            pos = (word[0][3][1] - word[0][0][1]) / 2 + word[0][0][1]
            value = float(word[1].replace(",", "."))
            fvfm_value_list.append([pos, value])
    if len(fvfm_value_list) >= 2:
        fvfm_value_list.sort(key=lambda x: x[0])
        return fvfm_value_list
    else:
        raise ValueError("Cannot find Fv/Fm value.")
