"""Contains example data for dana plots.

All functions starting with "df" can be accessed via the cli, example:
py -m dana df_sincos
will plot the dataframe created by df_sincos
"""

from functools import cache
from math import cos, sin

import pandas as pd


@cache
def df_sincos():
    """Create a small dataframe with a sine and cosine wave."""
    X = tuple(x * 0.05 for x in range(1000))
    Y = tuple(sin(x) for x in X)
    df = pd.DataFrame({"x": X, "sin_x": Y})
    df = df.set_index("x", drop=True)
    df["cos_x"] = tuple(cos(x) for x in X)

    return df
