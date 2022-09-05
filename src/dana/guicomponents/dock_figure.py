from . import dock as _D
from pyqtgraph.Qt import QtWidgets
from dana.guicomponents.betterlineedit import BetterlineEdit as BLE
import dana.guicomponents.bettertreeview as BTV


class Dock(_D.Dock):
    def __init__(self, pos=None):
        super().__init__("figure", pos=pos, closable=True)

    def showPlot(self, w):
        for idx in range(self.layout.count()):
            self.layout.removeItem(self.layout.itemAt(idx))
        self.addWidget(w)
