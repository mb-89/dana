import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets

from dana.datavis.betterlegend import Betterlegend


class PlotWidget(pg.GraphicsLayoutWidget):
    def __init__(self, plotinfo, data, args={}):
        super().__init__()
        self.currLayout = {}
        self.fillPlots(plotinfo, data, args={})

    def fillPlots(self, plotinfo, data, args):
        newLayout = self.distributePlots(plotinfo, data, args)
        for k, v in newLayout.items():
            if v == self.currLayout.get(k):
                continue
        self.currLayout = newLayout
        no = 1
        for k, v in self.currLayout.items():
            row = no - 1 % 3
            col = (no - 1) // 3
            no += 1
            self.pltItem = PltItemWithCursors(v, data, args)
            self.addItem(self.pltItem, row=row, col=col)

    def distributePlots(self, pi, data, args):
        """
        create a dict.
        The key is the plot (1...9).
        The value is a list.
        Every entry in the list has 3 subentries:
        subentry 1: h5 key
        subentry 2: x ax key and column nr (tuple) (or None)
        subentry 3: y ax key and column nr (tuple)
        """
        dct = {}
        xax = pi["dss"].get(0)
        for subplot in range(1, 10):
            if subplot not in pi["dss"]:
                continue
            plt = []
            for DF in pi["dfs"]:
                for yidx in pi["dss"][subplot]:
                    X = None  # TBD: add proper x axis support
                    idxs = data.getIndexData(DF)
                    if yidx not in idxs:
                        continue
                    Y = (yidx, idxs.index(yidx))
                    plt.append((DF, X, Y))
            dct[subplot] = plt
        return dct


class PltItemWithCursors(pg.PlotItem):
    def __init__(self, plotinfo, data, args):
        super().__init__()
        self.initialized = False
        A = 65
        self.showGrid(1, 1, int(0.75 * 255))
        self.customlegend = Betterlegend(
            "x",
            pen=pg.mkPen(255, 255, 255, A),
            brush=pg.mkBrush(0, 0, 255, A),
            offset=(70, 20),
        )
        self.customlegend.setParentItem(self)
        self.setTitle("")

        L = len(plotinfo)
        for idx, (key, X, Y) in enumerate(plotinfo):
            Ydata = data.getData(key)[:, Y[1]]
            Xdata = None  # TBD: Add proper x data support
            self.plot(Ydata, name=f"{Y[0]} @ {key}", pen=(idx + 1, L))

        self.initialized = True

    def plot(self, *args, **kwargs):
        p = super().plot(*args, **kwargs)
        self.customlegend.addItem(p, kwargs["name"])
        return p
