"""Classic line plots."""

from dana.lineplot.widgets import PlotBuilder


def createPlot(df, *args, **kwargs):
    """Give public access to the plot builder."""
    p = PlotBuilder().buildPlot(df, *args, **kwargs)
    return p
