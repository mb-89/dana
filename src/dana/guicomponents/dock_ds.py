from . import dock as _D
from pyqtgraph.Qt import QtCore, QtWidgets, QtGui
from dana.guicomponents.betterlineedit import BetterlineEdit as BLE

import pyqtgraph as pg

dfqueryLink = "pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html"


class Dock(_D.Dock):
    def __init__(self, pos=None):
        super().__init__("dataseries", pos=pos)
        self.filt = BLE("filter query", f"help: {dfqueryLink}")
        self.sel = BLE("selection query", f"help: {dfqueryLink}")

        self.addWidget(self.filt)
        self.addWidget(self.sel)
        self.addWidget(self.createBTV())

        pol = QtWidgets.QSizePolicy.Policy
        self.layout.parentWidget().setSizePolicy(pol.Preferred, pol.MinimumExpanding)

        self.filt.valueChanged.connect(self.loadData)
        self.sel.valueChanged.connect(self.selectData)
        self.getdata = pg.mkQApp().data.getIndexDataFrame

    def startup(self):
        self.loadData()
