import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets

import dana.guicomponents.bettertreeview as BTV
from dana.guicomponents.betterlineedit import BetterlineEdit as BLE

from . import dock as _D

dfqueryLink = "pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html"


class Dock(_D.BetterDock):
    def __init__(self, pos=None):
        super().__init__("plots", pos=pos)

        self.addPlotLines()
        pg.mkQApp().gui.numberkeypressed.connect(self.assignAxContent)

    def addPlotLines(self):
        pol = QtWidgets.QSizePolicy.Policy
        self.layout.parentWidget().setSizePolicy(pol.Preferred, pol.Maximum)
        self.plotsels = []
        for idx in range(10):
            p = BLE(f"selection query for axis {idx}", f"help: {dfqueryLink}")
            self.addWidget(p)
            self.plotsels.append(p)

    def assignAxContent(self, ax):
        srcdock = pg.mkQApp().gui.docks["dataseries"]
        nextxt = srcdock.sel.currentText()
        currtxt = self.plotsels[ax].currentText()
        if nextxt == currtxt:
            nextxt = ""
        self.plotsels[ax].setCurrentText(nextxt)
