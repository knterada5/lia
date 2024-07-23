"""Calculate ratio."""

import itertools
import statistics

import numpy as np


def calculate_ratio(fvfm_value_list):
    """Calculate height per fvfm value 1 from value.

    Parameters
    ----------
    fvfm_value_list : [[float, int], ...]
        List of position hight and Fv/Fm value.

    Returns
    -------
    scale : float
        Standard scale of Fv/Fm value.

    Raises
    ------
    ValueError
        If no value.
    """
    scale_list = []
    for pair in itertools.combinations(fvfm_value_list, 2):
        pos_diff = np.abs(pair[1][0] - pair[0][0])
        val_diff = np.abs(pair[0][1] - pair[1][1])
        scale = pos_diff / val_diff
        scale_list.append(scale)
    if len(scale_list) > 0:
        scale = statistics.median(scale_list)
        return scale
    else:
        raise ValueError("Cannot calculate scale. Not enough value.")
