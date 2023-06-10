"""Basic example on how to plot a csv file with the dana backend."""
import tempfile as tf
from pathlib import Path

import dana as da
import dana.exampledata as ex

df = ex.df_sincos()
plts = []

with tf.TemporaryDirectory() as td:
    f = Path(td) / "tmp.csv"
    df.to_csv(f)
    plts.extend(da.plotfiles([f]))

# if we store the data in a nonstandard format,
# we must pass the format information to plotfiles,
# so we can read it.
with tf.TemporaryDirectory() as td:
    f = Path(td) / "tmp.csv"
    df.to_csv(f, sep="|")
    plts.extend(da.plotfiles([f], {"sep": "|"}))

for p in plts:
    p.show()

if __name__ == "__main__":
    p.exec()
