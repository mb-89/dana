from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph.Qt import QtCore, QtWidgets, QtGui
from dana.guicomponents.bettertreeview import Bettertreeview, Bettermdl
import pyqtgraph as pg


class DatatreeDock(Dock):
    plotMetaSignal = QtCore.Signal()
    plotSignal = QtCore.Signal(str)

    def __init__(self):
        super().__init__("Datatree")
        self.mdl = QtGui.QStandardItemModel()
        self.fmdl = Bettermdl()
        self.fmdl.setSourceModel(self.mdl)
        self.view = Bettertreeview()
        self.view.setModel(self.fmdl)
        self.filterEdit = QtWidgets.QComboBox()
        self.filterEdit.setEditable(True)
        self.filterEdit.lineEdit().returnPressed.connect(self.filter)
        self.filterEdit.currentIndexChanged.connect(self.filter)
        self.filterEdit.lineEdit().setPlaceholderText(
            "filter query (help: pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html)"
        )
        self.lastFilter = None
        self.buttons = self.mkButtons()

        self.addWidget(self.filterEdit)
        self.addWidget(self.view)
        self.addWidget(self.buttons)

    def mkButtons(self):
        w = QtWidgets.QWidget()
        la = QtWidgets.QHBoxLayout()
        w.setLayout(la)
        la.setSpacing(0)
        la.setContentsMargins(0, 0, 0, 0)

        plotMeta = QtWidgets.QPushButton("PM")
        plotMetaAction = QtGui.QAction(self)
        plotMetaAction.setShortcut("F5")
        plotMeta.setToolTip("Plot Metadata [F5]")
        plotMeta.clicked.connect(plotMetaAction.trigger)
        plotMetaAction.triggered.connect(lambda: self.plotMetaSignal.emit())
        self.addAction(plotMetaAction)
        la.addWidget(plotMeta)

        plot = QtWidgets.QPushButton("P")
        plotAction = QtGui.QAction(self)
        plotAction.setShortcut("F9")
        plot.setToolTip("Plot Data [F9]")
        plot.clicked.connect(plotAction.trigger)
        plotAction.triggered.connect(lambda: self.plotSignal.emit(self.lastFilter))
        self.addAction(plotAction)
        la.addWidget(plot)

        return w

    def startup(self):
        self.updateMdl()

    def filter(self):
        txt = self.filterEdit.currentText()
        if txt == self.lastFilter:
            return
        self.lastFilter = txt
        self.updateMdl(txt)

    def updateMdl(self, filt=""):
        data = pg.mkQApp().data.getMetaDataFrame(filt=filt)
        self.fmdl.updateMdl(data)
        self.view.header.setStretchLastSection(True)
