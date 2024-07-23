"""Convert data for graphing."""

from lia.dataframe.add import add_hue
from lia.fvfm.get_unique import get_unique_px
from lia.fvfm.to_dataframe import to_bgr_and_fvfm_dataframe
from lia.graph.color import to_graph_rgb


def input_data_for_graph(px, fvfm_value):
    """Prepare input data for graphing.

    Parameters
    ----------
    px : [[int, int, int], ...]
        List of BGR values per pixel.
    fvfm_value : [int, ...]
        Fv/Fm value corresponding to each pixel.

    Returns
    -------
    blue : [int, ...]
        List of blue value.
    green : [int, ...]
        List of green value.
    red : [int, ...]
        List of red value.
    color : [str, ...]
        List of color for graph.
    hue : [int, ...]
        List of hue value.
    fvfm : [int, ...]
        List of Fv/Fm value.
    """
    # Convert to data frame to remove duplicates.
    df = to_bgr_and_fvfm_dataframe(px, fvfm_value)
    uniq_df = get_unique_px(df)
    df_hue = add_hue(uniq_df)
    blue = df_hue["blue"]
    green = df_hue["green"]
    red = df_hue["red"]
    hue = df_hue["hue"]
    fvfm = df_hue["fvfm"]
    color_list = df_hue[["red", "green", "blue"]].to_numpy().tolist()
    color = to_graph_rgb(color_list)
    return blue, green, red, color, hue, fvfm
