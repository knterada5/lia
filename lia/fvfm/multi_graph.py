"""Summarize the three graphs."""

from plotly.subplots import make_subplots


def make_multi_graph(fig_fvfm2d, fig_color3d, fig_fvfm3d):
    """Summarize the three graphs.

    Parameters
    ----------
    fig_fvfm2d : plotly.graph_objects.Figure
        2D scatter figure of Hue and Fv/Fm.
    fig_color3d : plotly.graph_objects.Figure
        3D scatter figure of leaf color.
    fig_fvfm3d : plotly.graph_objects.Figure
        3D scatter figure of leaf color and Fv/Fm value.

    Returns
    -------
    fig_multi : plotly.graph_objects.Figure
        Summarized graph.
    """
    fig_multi = make_subplots(
        rows=1,
        cols=3,
        specs=[[{"type": "xy"}, {"type": "scatter3d"}, {"type": "scatter3d"}]],
        subplot_titles=["Hue and Fv/Fm", "Leaf color", "Leaf color and Fv/Fm"],
    )
    fig_multi.add_trace(fig_fvfm2d["data"][0], row=1, col=1)
    fig_multi.add_trace(fig_color3d["data"][0], row=1, col=2)
    fig_multi.add_trace(fig_fvfm3d["data"][0], row=1, col=3)
    scene = {
        "xaxis": {"title": "Blue", "range": [0, 255]},
        "yaxis": {"title": "Green", "range": [0, 255]},
        "zaxis": {"title": "Red", "range": [0, 255]},
        "aspectratio": {"x": 1, "y": 1, "z": 1},
    }
    fig_multi.update_layout(
        showlegend=False,
        xaxis={"title": "Hue"},
        yaxis={"title": "Fv/Fm"},
        scene=scene,
        scene2=scene,
    )
    return fig_multi
