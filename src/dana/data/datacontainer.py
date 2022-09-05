import json
from itertools import chain

import h5py
import pandas as pd

from dana.data import examples


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
                idxname = v.index.name
                cols = v.columns
                self.store[k] = v.reset_index()
                self.store[k].attrs["indexdata"] = json.dumps([idxname] + list(cols))
                self.store[k].attrs["metadata"] = json.dumps(v.attrs)

    def getKeys(self):
        return self.store.keys()

    def getData(self, key):
        return self.store[key]

    def getMetaData(self, key):
        return json.loads(self.store[key].attrs.get("metadata", "{}"))

    def getIndexData(self, key):
        return json.loads(self.store[key].attrs.get("indexdata", "[]"))

    def getMetaDataColumns(self):
        cols = set(
            chain.from_iterable(self.getMetaData(y).keys() for y in self.getKeys())
        )
        return sorted(cols)

    def getMetaDataFrame(self, filt=""):
        keys = self.getKeys()
        df = pd.DataFrame(self.getMetaData(x) for x in keys).reset_index(drop=True)
        df["key"] = keys
        df["index"] = [f"df{str(idx).zfill(4)}" for idx in range(len(keys))]
        df.insert(0, "index", df.pop("index"))
        df.set_index("key", inplace=True)
        if filt:
            try:
                df = df.query(filt)
            except:
                pass
        return df

    def getIndexDataFrame(self, filt=""):
        keys = self.getKeys()
        indices = set(chain.from_iterable(self.getIndexData(y) for y in keys))

        df = pd.DataFrame()
        df["index"] = [f"ds{str(idx).zfill(4)}" for idx in range(len(indices))]
        df["key"] = sorted(indices)
        df.set_index("key", inplace=True)
        if filt:
            try:
                df = df.query(filt)
            except:
                pass
        return df
