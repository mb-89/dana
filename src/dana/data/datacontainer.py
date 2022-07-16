import json

import h5py

from dana.data import examples
from itertools import chain
import pandas as pd


class Datacontainer:
    def __init__(self):
        self.srcs = []
        self.store = h5py.File("dana_ramdisk", "a", driver="core", backing_store=False)

    def open(self, src: str) -> None:
        if src in self.srcs:
            return
        self.srcs.append(src)
        if src == "#example":
            for k, v in examples.getExampleData(src):
                self.store[k] = v
                self.store[k].attrs["metadata"] = json.dumps(v.attrs)

    def getKeys(self):
        return self.store.keys()

    def getData(self, key):
        return self.store[key]

    def getMetaData(self, key):
        return json.loads(self.store[key].attrs.get("metadata", "{}"))

    def getMetaDataColumns(self):
        cols = set(
            chain.from_iterable(self.getMetaData(y).keys() for y in self.getKeys())
        )
        return sorted(cols)

    def getMetaDataFrame(self, filt=""):
        keys = self.getKeys()
        df = pd.DataFrame(self.getMetaData(x) for x in keys).reset_index()
        df["key"] = keys
        df.set_index("key", inplace=True)
        if filt:
            try:
                df = df.query(filt)
            except:
                pass
        return df
