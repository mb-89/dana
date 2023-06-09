"""Basic example on how to plot a dataframe with the dana backend."""

import dana as da
import dana.exampledata as ex

df = ex.df_sincos()

p = df.plot(backend="dana", title="Basic example")
p.show()

if __name__ == "__main__":
    da.exec()
