"""Basic example on how to plot a dataframe with the dana backend."""
from math import sin

import pandas as pd

import dana as da

X = tuple(x * 0.05 for x in range(1000))
Y = tuple(sin(x) for x in X)

df = pd.DataFrame({"x": X, "sin_x": Y})
df = df.set_index("x", drop=True)

p = df.plot(backend="dana", title="Basic example")
p.show()

if __name__ == "__main__":
    da.exec()
