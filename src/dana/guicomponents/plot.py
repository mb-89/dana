from pyqtgraph.dockarea.Dock import Dock


class PlotDock(Dock):
    def __init__(self, filt):
        super().__init__("Plot", closable=True)
