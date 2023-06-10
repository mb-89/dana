"""Decison trees."""

from dana.decisiontree.widgets import PlotBuilder


def createPlot(df, *args, **kwargs):
    """Give public access to the plot builder."""
    p = PlotBuilder().buildPlot(df, *args, **kwargs)
    return p
