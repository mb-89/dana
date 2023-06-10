"""Contains example data for dana plots.

All functions starting with "df" can be accessed via the cli, example:
py -m dana df_sincos
will plot the dataframe created by df_sincos
"""

from functools import cache

import numpy as np
import pandas as pd


@cache
def df_sincos():
    """Create a small dataframe with a sine and cosine wave."""
    X = tuple(x * 0.05 for x in range(1000))
    Y = np.sin(X)
    df = pd.DataFrame({"x": X, "sin_x": Y})
    df = df.set_index("x", drop=True)
    df["cos_x"] = np.cos(X)

    return df


@cache
def df_parameterstudy_regression():
    """Create a df where one col is a measure of quality as a function of others."""
    # from sklearn import datasets
    # rawdata = datasets.load_boston()
    # df = pd.DataFrame(data=rawdata.data, index=rawdata.target)
    # df.columns = rawdata.feature_names
    # df.index.name = Path(rawdata.filename).stem

    df = pd.DataFrame()
    df["x1"] = np.linspace(0, 5, 500)
    df["x2"] = np.linspace(-1, 1, 500)
    df["x3"] = np.linspace(1, 1500, 500)
    df["x4"] = np.linspace(-10, 10, 500)

    # as with error norms, assume 0 = perfect
    df["q"] = np.abs(1 / (df.x1 * np.abs(df.x2) * 5 * np.sqrt(df.x3) + df.x4))
    df = df.set_index("q", drop=True)

    return df
