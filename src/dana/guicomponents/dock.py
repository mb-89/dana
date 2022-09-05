from functools import partial

import pyqtgraph as pg
from pyqtgraph.dockarea.Dock import Dock as _D
from pyqtgraph.dockarea.DockArea import DockArea as _DA
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

import dana.guicomponents.bettertreeview as BTV
from dana.datavis.defaultPlot import PlotWidget


class BetterDockArea(_DA):
    numberkeypressed = QtCore.Signal(int)

    def __init__(self):
        super().__init__()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.installActions()

    def startup(self):
        for d in self.docks.values():
            d.startup()

    def installActions(self):
        self.actions = []

        for idx in range(10):
            setAxContent = QtGui.QAction(f"assign to axis &{idx}", self)
            setAxContent.setShortcut(str(idx))
            p = partial(self.numberkeypressed.emit, idx)
            setAxContent.triggered.connect(p)
            self.actions.append(setAxContent)
            self.addAction(setAxContent)

        plotAction = QtGui.QAction(f"plot selected series", self)
        plotAction.setShortcut("F5")
        plotAction.triggered.connect(self.createPlot)
        self.actions.append(plotAction)
        self.addAction(plotAction)

    def createPlot(self):
        app = pg.mkQApp()
        plotinfo = self.createPlotInfo()
        w = PlotWidget(plotinfo, app.data, app.args)
        self.docks["figure"].showPlot(w)

    def createPlotInfo(self):
        dfsel = self.docks["dataframes"].getSelectedIdxs()
        ds = self.docks["dataseries"].getdata()
        axes = [x.currentText() for x in self.docks["plots"].plotsels]
        dssel = {}
        for idx, ax in enumerate(axes):
            if not ax:
                continue
            dssel[idx] = tuple(ds.query(ax).index.values)
        return {"dfs": dfsel, "dss": dssel}


class BetterDock(_D):
    selectionExprChanged = QtCore.Signal(str)

    def __init__(self, name, pos=None, **kwargs):
        super().__init__(name, **kwargs)
        if pos is None:
            ("top", None)
        self.pos = pos
        self.getdata = lambda x: None
        self._ignoreTxtChanges = False

    def startup(self):
        pass

    def createButtons(self):
        w = QtWidgets.QWidget()
        la = QtWidgets.QGridLayout()
        la.setSpacing(0)
        la.setContentsMargins(0, 0, 0, 0)
        w.setLayout(la)

        buttons = [QtWidgets.QPushButton("") for x in range(27)]

        buttonsperRow = 3
        for idx, button in enumerate(buttons):
            row = idx // buttonsperRow
            col = idx % buttonsperRow
            la.addWidget(button, row, col)
        la.setRowStretch(la.rowCount(), 1)

        self.layout.setColumnStretch(0, 3)
        self.layout.setColumnStretch(1, 1)
        return w

    def createBTV(self):
        self.mdl = BTV.Bettermdl()
        self.view = BTV.Bettertreeview()
        self.view.selectionChanged.connect(self.onSelChange)
        self.view.setModel(self.mdl)

        return self.view

    def onSelChange(self, newsel):
        newsel = [x for x in newsel if x.column() == 0]
        key = self.mdl.headerData(0, QtCore.Qt.Horizontal)
        selstr = f"{key} in [" + ",".join(f'"{k.data(0)}"' for k in newsel) + "]"
        if not self._ignoreTxtChanges:
            self.selectionExprChanged.emit(selstr)

    def loadData(self, filt=""):
        data = self.getdata(filt)
        self.mdl.updateMdl(data)
        self.view.header.setStretchLastSection(True)

    def selectData(self, filt=""):
        data = self.getdata(filt)
        selection = list(data.index)
        sm = self.view.selectionModel()
        smclass = QtCore.QItemSelectionModel
        self._ignoreTxtChanges = True
        sm.clearSelection()
        for row in range(self.mdl.rowCount()):
            idx = self.mdl.index(row, 0)
            if idx.data(0) not in selection:
                continue
            sm.select(idx, smclass.Rows | smclass.Select)
        self._ignoreTxtChanges = False

    def getSelectedIdxs(self):
        sm = self.view.selectionModel()
        return tuple(x.data(0) for x in self.view.selectionModel().selectedRows(0))
