import PySide6  # noqa: F401 # isort:skip
import pyqtgraph as pg  # isort:skip

from pyqtgraph.Qt import QtCore, QtWidgets
from dana.guicomponents import dock, dock_df, dock_ds, dock_p, dock_figure

from . import __metadata__, api


def show(args):
    gui = mkgui(args)
    gui.show()
    pg.exec()


def mkgui(args):
    app = pg.mkQApp(__metadata__.__projname__)
    win = QtWidgets.QMainWindow()
    win.resize(1000, 800)
    docks = dock.DockArea()
    win.setCentralWidget(docks)
    win.setWindowTitle(__metadata__.__projname__)
    win.setStatusBar(QtWidgets.QStatusBar())

    app.data = api.getDatacontainer()
    app.args = args
    app.gui = docks

    mkDocks(app)

    QtCore.QTimer.singleShot(0, startup)

    return win


def mkDocks(app):
    dfdock = dock_df.Dock(pos=("left", None))
    dsdock = dock_ds.Dock(pos=("bottom", dfdock))
    pdock = dock_p.Dock(pos=("bottom", dsdock))
    fdock = dock_figure.Dock(pos=("right", None))
    area = app.gui
    for d in [dfdock, dsdock, pdock, fdock]:
        area.addDock(d, *d.pos)


def startup():
    app = pg.mkQApp()
    args = app.args
    for src in args["srcs"]:
        app.data.open(src)
    app.gui.startup()
