from pyqtgraph.Qt import QtWidgets

import dana.guicomponents.bettertreeview as BTV
from dana.guicomponents.betterlineedit import BetterlineEdit as BLE

from . import dock as _D


class Dock(_D.BetterDock):
    def __init__(self, pos=None):
        super().__init__("figure", pos=pos, closable=True)

    def showPlot(self, w):
        for idx in range(self.layout.count()):
            self.layout.removeItem(self.layout.itemAt(idx))
        self.addWidget(w)
