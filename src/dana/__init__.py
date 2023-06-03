"""Analyzes and plots data."""

import pyqtgraph as pg

exec = pg.exec


def plot(data, kind, **kwargs):
    """Provide an entry point for pandas.

    | Can be executed via:
    | import dana
    | import pandas as pd
    | pd.DataFrame().plot(backend="dana").

    We add the entry point dynamically, so it also works in editable mode:
    https://stackoverflow.com/a/48666503
    """
    p = data.plot(backend="matplotlib", kind=kind, **kwargs)

    if not isinstance(p, pg.QtWidgets.QWidget):
        p = _wrapInWidget(p)

    return p


def _addEntryPoint():
    """Register the pandas entry point on import."""
    import pkg_resources

    d = pkg_resources.Distribution(__file__)
    ep = pkg_resources.EntryPoint.parse("dana = dana:plot", dist=d)
    d._ep_map = {"pandas_plotting_backends": {"dana": ep}}
    pkg_resources.working_set.add(d, "dana")


def _wrapInWidget(p):
    """Wrap the output of the default plotter in a QWidget."""
    from matplotlib.backends.backend_qtagg import FigureCanvas
    from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NTB

    w = pg.QtWidgets.QWidget()
    la = pg.QtWidgets.QVBoxLayout(w)
    canvas = FigureCanvas(p.get_figure())
    la.addWidget(NTB(canvas, w))
    la.addWidget(canvas)

    return w


pg.mkQApp()
_addEntryPoint()
