import PySide6  # noqa: F401 # isort:skip
import pyqtgraph as pg  # isort:skip
from pyqtgraph.dockarea.DockArea import DockArea
from pyqtgraph.Qt import QtCore, QtWidgets

from dana.guicomponents import datatree, metaplot, plot

from . import __metadata__, api


def show(args):
    gui = mkgui(args)
    gui.show()
    pg.exec()


def mkgui(args):
    app = pg.mkQApp(__metadata__.__projname__)
    win = QtWidgets.QMainWindow()
    win.resize(1000, 800)
    docks = Docks()
    win.setCentralWidget(docks)
    win.setWindowTitle(__metadata__.__projname__)

    app.data = api.getDatacontainer()
    app.args = args
    app.gui = docks

    dtd = datatree.DatatreeDock()

    dockList = [(dtd, "top")]

    for d, pos in dockList:
        docks.addDock(d, pos)

    def startup():
        # read all data
        for src in args["srcs"]:
            app.data.open(src)
        # initialize all docks
        for d, _ in dockList:
            if hasattr(d, "startup"):
                d.startup()

    QtCore.QTimer.singleShot(0, startup)

    def addMetadataDock():
        mpd = metaplot.MetaplotDock()
        app.gui.addDock(mpd, "right", dtd)
        # mpd.float()

        def applyfiltfun(txt):
            dtd.filterEdit.setCurrentText(txt)
            dtd.filter()

        mpd.applyFilt.connect(applyfiltfun)

    def addPlotDock(filt):
        pd = plot.PlotDock(filt)
        app.gui.addDock(pd, "bottom", dtd)

    dtd.plotMetaSignal.connect(addMetadataDock)
    dtd.plotSignal.connect(addPlotDock)

    return win


class Docks(DockArea):
    def makeContainer(self, typ):
        new = super().makeContainer(typ)
        new.setChildrenCollapsible(False)
        return new
