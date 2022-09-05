from pyqtgraph.Qt import QtWidgets
import pyqtgraph as pg
from dana.datavis.betterlegend import Betterlegend


class PlotWidget(pg.GraphicsLayoutWidget):
    def __init__(self, plotinfo, data, args={}):
        super().__init__()
        self.fillPlots(plotinfo, data, args={})
        self.currLayout = {}
        self.plots = {}

    def fillPlots(self, plotinfo, data, args):
        newLayout = self.distributePlots(plotinfo, data, args)
        for k, v in newLayout:
            if v == self.currLayout.get(k):
                continue

        self.pltItem = PltItemWithCursors(plotinfo, data, args)
        self.addItem(self.pltItem, row=1, col=0)

        self.setData(plotinfo, data, args)


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
        self.initialized = True

    def plot(self, *args, **kwargs):
        p = super().plot(*args, **kwargs)
        self.customlegend.addItem(p, kwargs["name"])
        return p
