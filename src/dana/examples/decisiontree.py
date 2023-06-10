"""Basic example on how to plot decision tree with the dana backend."""

import graphviz  # noqa: F401 # needed so that graphs can be drawn

import dana as da  # noqa: F401 # to make the backend available, import dana
import dana.exampledata as ex

df = ex.df_parameterstudy_regression()

p = df.plot(backend="dana", kind="decision tree")
p.show()

if __name__ == "__main__":
    p.exec()
