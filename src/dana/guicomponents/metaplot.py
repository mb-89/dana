from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph.dockarea.DockArea import DockArea
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets, QtGui
import numpy as np
from PySide6 import QtWebEngineWidgets
import tempfile
import plotly.graph_objects as go
from pathlib import Path
import json


class MetaplotDock(Dock):
    applyFilt = QtCore.Signal(str)

    def __init__(self):
        super().__init__("Metaplot", closable=True)
        self.subdocks = MetaplotSubDocks()
        self.buttons = self.mkButtons()
        self.addWidget(self.subdocks)
        self.addWidget(self.buttons)

    def mkButtons(self):
        w = QtWidgets.QWidget()
        la = QtWidgets.QHBoxLayout()
        w.setLayout(la)
        la.setSpacing(0)
        la.setContentsMargins(0, 0, 0, 0)

        but = QtWidgets.QPushButton("AF")
        act = QtGui.QAction(self)
        act.setShortcut("F8")
        but.setToolTip("Apply Filter to datatree [F8]")
        but.clicked.connect(act.trigger)
        act.triggered.connect(self.subdocks.pcd.w.emitFiltQuery)
        self.subdocks.pcd.w.filtQuery.connect(self.applyFilt.emit)
        self.addAction(act)
        la.addWidget(but)

        return w


class MetaplotSubDocks(DockArea):
    def __init__(self):
        super().__init__()
        self.pcd = ParCoordDock()
        self.addDock(self.pcd, "top")


class ParCoordDock(Dock):
    def __init__(self):
        super().__init__("Parcoords")
        self.w = ParCoordWidget()
        self.addWidget(self.w)


class ParCoordWidget(QtWebEngineWidgets.QWebEngineView):
    filtQuery = QtCore.Signal(str)

    def __init__(self):
        super().__init__()

        self.td = tempfile.TemporaryDirectory()
        self.tempfile = self.td.name + "/tmp.html"
        self.colorscale = "Turbo"
        self._page = self.page()
        self.setParcoordData(pg.mkQApp().data.getMetaDataFrame())

    def setParcoordData(self, df):
        self.df = df
        dims = [dict(label=k, values=df[k]) for k in df.columns]
        order = np.argsort(dims[0]["values"])
        for idx in range(len(dims)):
            dims[idx]["values"] = dims[idx]["values"][order]
        self.calcMinMaxValues(df)

        colornumbers = [float(x) for x in dims[0]["values"]]
        line = dict(color=colornumbers, colorscale=self.colorscale)
        pc = go.Parcoords(dimensions=dims, line=line)
        fig = go.Figure(data=pc)
        fig.layout.template = "plotly_dark"
        html = fig.to_html()
        open(self.tempfile, "w").write(html)
        url = QtCore.QUrl.fromLocalFile(str(Path(self.tempfile).resolve()))
        self.load(url)

    def calcMinMaxValues(self, df):
        self.minmax = {}
        for k in df.columns:
            minval = min(df[k])
            maxval = max(df[k])
            self.minmax[k] = (minval, maxval, maxval - minval)

    def emitFiltQuery(self, axlims=None):
        if type(axlims) != str:
            return self.getAxLimits()
        lims = {}
        for k, v in json.loads(axlims).items():
            vs = v.split(",")
            if len(vs) <= 2:
                continue
            minval = float(vs[0])
            maxval = float(vs[-1])
            start = float(vs[1])
            end = start + float(vs[2])
            span = maxval - minval

            startrel = min(1, max(0, start - minval) / span)
            endrel = min(1, max(0, end - minval) / span)
            s, e, sp = self.minmax[k]
            lims[k] = (s + startrel * sp, s + endrel * sp)

        df = self.df
        for k, (minv, maxv) in lims.items():
            df = df[(df[k] >= minv) & (df[k] <= maxv)]

        filts = df["index"]
        self.filtQuery.emit(f"index in {list(filts)}")

    def getAxLimits(self):

        self._page.runJavaScript(
            """
        var prefixfun = (prefix) =>{if (prefix === 'svg'){
            return 'http://www.w3.org/2000/svg';}else{return null;}};
        (function () {
        res1 = document.evaluate(
        '//svg:line[@stroke-dasharray and @class="highlight"]/@stroke-dasharray',
                document,
                prefixfun,
                XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,null);

            res2 = document.evaluate(
                '//svg:g[@class="axis-heading"]',
                document,
                prefixfun,
                XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,null);

            var dct = {}
            for (let idx=0;idx<res1.snapshotLength;idx++){
                key = res2.snapshotItem(idx).textContent;
                val = res1.snapshotItem(idx).value
                dct[key] = val;
            }

            return JSON.stringify(dct)
            })();""",
            0,
            self.emitFiltQuery,
        )
