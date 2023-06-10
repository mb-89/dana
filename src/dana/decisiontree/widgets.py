"""Contains widgets used for decision trees."""
from pathlib import Path

import pyqtgraph as pg
from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph.dockarea.DockArea import DockArea

import dana as da
from dana import fun


class PlotBuilder:
    """A builder-pattern helper that creates decision trees."""

    def __init__(
        self,
    ) -> None:
        self.df = None
        self.srcname = "dana decision tree"
        self.target = None
        self.args = {}

    def buildPlot(self, df, *args, **kwargs):
        """Build the Plot. This is the main build function that is called from outside."""
        builder = self.setSrc(df, name=kwargs.get("title")).setParams(**kwargs)
        return builder.mk()

    def setParams(self, **kwargs):
        """Set parameters before building the widget."""
        self.args = kwargs
        return self

    def setSrc(self, df, name=None):
        """Set the source data for the plot."""
        self.df = df
        if name:
            self.srcname = name
        return self

    def mk(self):
        """Create the widgets for the plots.

        This function should always be called last during the build, as it
        works on the setup that was done with all ohter builder functions.
        """
        import dtreeviz
        from matplotlib.backends.backend_qtagg import FigureCanvas
        from matplotlib.backends.backend_qtagg import \
            NavigationToolbar2QT as NTB
        from sklearn.tree import DecisionTreeRegressor
        from yellowbrick.model_selection import FeatureImportances

        random_state = 1234  # for reproducible trees
        df = self.df

        self.args.setdefault("random_state", random_state)
        self.args.setdefault("max_depth", 3)
        self.args["max_depth"] = int(self.args["max_depth"])
        regr = fun.callWithKnownArgs(DecisionTreeRegressor, self.args)
        features = df.to_numpy()
        target = df.index.to_numpy()
        regr.fit(features, target)

        from PySide6 import QtWebEngineWidgets

        da.mkQApp()
        w = DockArea()

        # decision tree
        self.args["model"] = regr
        self.args["X_train"] = features
        self.args["y_train"] = target
        self.args["feature_names"] = df.columns
        self.args["target_name"] = df.index.name
        viz_rmodel = fun.callWithKnownArgs(dtreeviz.model, self.args)
        self.args.setdefault("orientation", "LR")
        v = fun.callWithKnownArgs(viz_rmodel.view, self.args)
        fn = v.save_svg()
        tree = QtWebEngineWidgets.QWebEngineView()
        url = pg.QtCore.QUrl.fromLocalFile(str(Path(fn).resolve()))
        tree.load(url)

        # importances
        imp = FeatureImportances(regr, labels=df.columns, show=False)
        plot = imp.fit(features, target)
        plot.finalize()
        iw = pg.QtWidgets.QWidget(w)
        la = pg.QtWidgets.QVBoxLayout(iw)
        canvas = FigureCanvas(plot.ax.get_figure())
        la.addWidget(NTB(canvas, iw))
        la.addWidget(canvas)

        treedock = Dock("decision tree")
        treedock.addWidget(tree)
        w.addDock(treedock, "left")
        treedock = Dock("importances")
        treedock.addWidget(canvas)
        w.addDock(treedock, "right")
        return w
