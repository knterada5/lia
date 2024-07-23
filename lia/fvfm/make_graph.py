"""Make graph of leaf color and Fv/Fm value."""

from lia.graph.make_graph import make_2dscatter, make_3dscatter


def draw_graph(blue, green, red, color, hue, fvfm, name=None, fvfm_range=None):
    """Draw graphs of leaf color and Fv/Fm value.

    Parameters
    ----------
    blue : [int, ...]
        Blue, X axis.
    green : [int, ...]
        Green, Y axis.
    red : [int, ...]
        Red, Z axis.
    color : [[int, int, int], ...]
        List of BGR color.
    hue : [int, ...]
        Hue.
    fvfm : [float, ...]
        Fv/Fm value.
    name : str, optional
        Sample name.
    fvfm_range : (int, int), optional
        Range of Fv/Fm scalebar.

    Returns
    -------
    fig_fvfm2d : plotly.graph_objects.Figure
        2D scatter figure of Hue and Fv/Fm.
    fig_color3d : plotly.graph_objects.Figure
        3D scatter figure of leaf color.
    fig_fvfm3d : plotly.graph_objects.Figure
        3D scatter figure of leaf color and Fv/Fm value.
    """
    fvfm2d_figure_name = "2D scatter of Hue and Fv/Fm value " + name
    fig_fvfm2d = make_2dscatter(
        x=hue,
        y=fvfm,
        xaxis_title="Hue",
        yaxis_title="Fv/Fm",
        fig_title=fvfm2d_figure_name,
        marker_color=color,
    )
    color3d_figure_name = "3D scatter of leaf color " + name
    fig_color3d = make_3dscatter(
        x=blue,
        y=green,
        z=red,
        xaxis_title="Blue",
        yaxis_title="Green",
        zaxis_title="Red",
        xaxis_range=(0, 255),
        yaxis_range=(0, 255),
        zaxis_range=(0, 255),
        fig_title=color3d_figure_name,
        marker_color=color,
    )
    fvfm3d_figure_name = "3D scatter of leaf color and Fv/Fm value " + name
    fig_fvfm3d = make_3dscatter(
        x=blue,
        y=green,
        z=red,
        xaxis_title="Blue",
        yaxis_title="Green",
        zaxis_title="Red",
        xaxis_range=(0, 255),
        yaxis_range=(0, 255),
        zaxis_range=(0, 255),
        fig_title=fvfm3d_figure_name,
        marker_color=fvfm,
        colorbar_title="Fv/Fm",
        colorbar_range=fvfm_range,
    )
    return fig_fvfm2d, fig_color3d, fig_fvfm3d
