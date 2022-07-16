from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

ROLE_DISPLAY = QtCore.Qt.DisplayRole
ROLE_USER = QtCore.Qt.UserRole


class Header(QtWidgets.QHeaderView):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        # self.button = QtWidgets.QPushButton("F", self)
        # self.button.setMaximumWidth(20)


class Bettertreeview(QtWidgets.QTreeView):
    def __init__(self):
        super().__init__()
        self.header = Header(QtCore.Qt.Horizontal, self)
        self.setHeader(self.header)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)


class Bettermdl(QtCore.QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.cols = []

    def updateMdl(self, df):
        mdl = self.sourceModel()
        mdl.clear()
        root = mdl.invisibleRootItem()

        for idx, row in df.iterrows():
            item = QtGui.QStandardItem(idx)
            item.setEditable(False)
            for colno, colval in enumerate(row):
                item.setData(str(colval), ROLE_USER + colno + 1)

            root.appendRow([item])
        self.cols = ["key"] + list(df.columns)
        mdl.setHorizontalHeaderLabels(self.cols)

    def data(self, idx, role):
        if role != ROLE_DISPLAY:
            return super().data(idx, role)
        col = idx.column()
        if col == 0:
            ret = super().data(idx, role)
            return ret
        role = ROLE_USER + col
        return super().data(idx.siblingAtColumn(0), role)

    def sort(self, col, order):
        if not self.cols:
            return super().sort(col, order)
        r = ROLE_USER + col
        if col == 0:
            r = ROLE_DISPLAY
        self.setSortRole(r)
        col = 0
        return super().sort(col, order)
