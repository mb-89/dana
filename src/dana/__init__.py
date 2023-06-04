"""Analyzes and plots data."""

import PySide6  # noqa: F401


def plot(data, kind, **kwargs):
    """Plot the given dataframe."""
    import pyqtgraph as pg

    try:
        from IPython import get_ipython

        ipy = get_ipython()
    except ImportError:  # pragma: no cover / only needed on some venvs
        ipy = None
    """Provide an entry point for pandas.

    | Can be executed via:
    | import dana
    | import pandas as pd
    | pd.DataFrame().plot(backend="dana").

    We add the entry point dynamically, so it also works in editable mode:
    https://stackoverflow.com/a/48666503
    """

    match kind:
        case "line":
            from dana.lineplot import createPlot

            p = createPlot(data, **kwargs)
        case _:
            p = data.plot(backend="matplotlib", kind=kind, **kwargs)

    if not isinstance(p, pg.QtWidgets.QWidget):
        p = _wrapInWidget(p)

    if ipy is not None:  # pragma: no cover / only needed in interactive mode
        ipy.magic("gui qt")

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
    import pyqtgraph as pg
    from matplotlib.backends.backend_qtagg import FigureCanvas
    from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NTB

    w = pg.QtWidgets.QWidget()
    la = pg.QtWidgets.QVBoxLayout(w)
    canvas = FigureCanvas(p.get_figure())
    la.addWidget(NTB(canvas, w))
    la.addWidget(canvas)

    return w


def exec():  # pragma: no cover: only called when directly used in foreign scripts
    """Execute the qt event loop."""
    import pyqtgraph as pg

    pg.exec()


def mkQApp():
    """Create a qt app. Needed before constructing any widgets."""
    import pyqtgraph as pg

    pg.mkQApp()


mkQApp()
_addEntryPoint()
