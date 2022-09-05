from pyqtgraph.Qt import QtCore, QtGui, QtWidgets


class BetterlineEdit(QtWidgets.QComboBox):
    valueChanged = QtCore.Signal(str)

    def __init__(self, placeholder="", tooltip=""):
        super().__init__()
        self.setEditable(True)
        self.lineEdit().returnPressed.connect(self.updateVal)
        self.currentIndexChanged.connect(self.updateVal)

        self.lineEdit().setPlaceholderText(placeholder)
        self.lineEdit().setToolTip(tooltip)
        self.lastval = None

    def updateVal(self):
        val = self.currentText()
        if val == self.lastval:
            return
        self.lastFilter = val
        self.valueChanged.emit(val)
