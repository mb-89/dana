"""Contains widgets used for lineplots."""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets


class PlotBuilder:
    """A builder-pattern helper that creates lineplots."""

    def buildPlot(self, df, *args, **kwargs):
        """Build the Plot. This is the main build function that is called from outside."""
        plugins = [CursorPlugin]
        pluginOverride = kwargs.get("plugins")
        if pluginOverride is not None:
            plugins = pluginOverride

        builder = self.setSrc(df, name=kwargs.get("title")).addPlugins(plugins)
        return builder.mk()

    def __init__(self) -> None:
        self.df = None
        self.srcname = "dana lineplot"
        self.plugins = []

    def setSrc(self, df, name=None):
        """Set the source data for the plot."""
        self.df = df
        if name:
            self.srcname = name
        return self

    def addPlugins(self, plugins):
        """Add plugins to the plot, for example cursors, fft, ..."""
        self.plugins.extend(plugins)
        return self

    def mk(self):
        """Create the widgets for the plots.

        This function should always be called last during the build, as it
        works on the setup that was done with all ohter builder functions.
        """
        df = self.df
        w = DanaWidget()
        g = DanaGraphicsLayoutWidget(w)
        w.setWindowTitle(self.srcname)

        p1 = DanaPlotItem()
        g.addItem(p1)
        L = len(df.columns)
        if not L:
            return w
        if n := df.index.name:
            p1.setLabel("bottom", n)
        for idx, col in enumerate(df.columns):
            pen = (idx + 1, L)
            p1.plot(x=df.index, y=df[col], name=col, pen=pen)

        for p in self.plugins:
            w.addPlugin(p)

        w.addGraphics(g)

        self._finishLayout(w)
        return w

    def _finishLayout(self, w):
        w.pluginLa.addStretch()
        w.shortcuts = []
        for idx, (_, b) in enumerate(w.plugins.values()):
            sc = QtGui.QShortcut(QtGui.QKeySequence(f"F{idx+1}"), w)
            sc.activated.connect(b.click)
            w.shortcuts.append(sc)

        pw = w.pluginLa.parent()
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Window, QtCore.Qt.black)
        pw.setAutoFillBackground(True)
        pw.setPalette(pal)

        if not w.plugins:
            pw.setVisible(False)


class DanaWidget(QtWidgets.QWidget):
    """Subclass of QWidget with some convenience modifications."""

    def __init__(self):
        super().__init__()
        la = pg.QtWidgets.QGridLayout()
        cleanupSpacing(la)
        self.setLayout(la)
        self.la = la
        self.plugins = {}
        self.pluginLa = QtWidgets.QVBoxLayout()
        cleanupSpacing(self.pluginLa)
        w = QtWidgets.QWidget()
        w.setLayout(self.pluginLa)
        self.la.addWidget(w, 0, 1)

    def addPlugin(self, plugincls):
        """Integrate a plugin in the Gui."""
        name = plugincls.name
        if name not in self.plugins:
            p = plugincls(self)
            b = p.getButton()
            self.pluginLa.addWidget(b)
            self.plugins[name] = (p, b)

    def addGraphics(self, graphics):
        """Add the graphics layout that contains all plots."""
        self.la.addWidget(graphics, 0, 0)


class DanaGraphicsLayoutWidget(pg.GraphicsLayoutWidget):
    """Subclass of GraphicsLayoutWidget with some convenience modifications."""

    pass


class DanaPlotItem(pg.PlotItem):
    """Subclass of PlotItem with some convenience modifications."""

    def __init__(
        self,
    ):
        super().__init__()
        self.addLegend()
        self.showGrid(1, 1, 0.6)


class DanaLegendItem(pg.LegendItem):
    """Subclass of LegendItem with more features."""

    pass


class DanaPlugin:
    """Generic class that describes a plugin.

    A plugin is an additional piece of code that modifies the default plots to add functionality
    """

    name = "generic plugin"

    def getButton(self):
        """Create a button that shows up in the gui, used to switch the plugin on/off."""
        button = pg.Qt.QtWidgets.QPushButton(self.name)
        button.clicked.connect(lambda: print(self.name))
        button.setCheckable(True)
        return button

    def __init__(self, widget):
        pass


class CursorPlugin(DanaPlugin):
    """Plugin that adds cursors to plot and legend."""

    name = "cursors"

    # step 1: every subplot receives two cursors that move relative to the viewport
    # step 2: the cursors print their position and values on movement
    # step 3: every plot recvs an improved legend
    # step 4: the legend shows the values of the cursors
    # step 5: make it all toggle-able through a button


class FFTPlugin(DanaPlugin):
    """Plugin that adds an interactive FFT."""

    name = "FFT"


class FiltPlugin(DanaPlugin):
    """Plugin that adds an interactive Filter."""

    name = "Filt"


def cleanupSpacing(la):
    """Clean up spacing consistently for all layouts."""
    la.setSpacing(0)
    la.setContentsMargins(0, 0, 0, 0)
