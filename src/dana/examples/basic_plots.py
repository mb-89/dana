"""Basic example on how to plot a dataframe with the dana backend."""

import numpy as np
import pandas as pd

import dana as da

pd.options.plotting.backend = "dana"

df = pd.DataFrame()
df.index = tuple(x * 0.01 for x in range(1000))
df["sin_x"] = np.sin(df.index)

p = df.plot()
p.show()

if __name__ == "__main__":
    da.exec()
