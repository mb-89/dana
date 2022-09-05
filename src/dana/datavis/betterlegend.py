import pyqtgraph as pg


class Betterlegend(pg.LegendItem):
    def __init__(self, xname, *args, **kwargs):
        kwargs["colCount"] = 1
        super().__init__(*args, **kwargs)
        self.layout.addItem(pg.LabelItem("Name"), 0, 1)
        self.layout.addItem(pg.LabelItem(" X"), 1, 0)
        self.layout.addItem(pg.LabelItem(xname), 1, 1)
        self.expanded = False
        self.w0 = None
        self.w1 = None

    def setVals(self, cursorIdx, vals):
        for vidx, v in enumerate(vals):
            targetItem = self.layout.itemAt(vidx + 1, cursorIdx + 2)
            targetItem._val = v

            targetItem.setText(getFixedLenString(v))
        if (
            self.layout.itemAt(1, 2)._val is not None
            and self.layout.itemAt(1, 3)._val is not None
        ):
            self.calcDerivativeVals()

    def calcDerivativeVals(self):
        for row in range(1, self.layout.rowCount()):
            v0 = self.layout.itemAt(row, 2)._val
            v1 = self.layout.itemAt(row, 3)._val
            delta = v1 - v0
            deltainv = 0 if delta == 0 else 1 / delta
            t = self.layout.itemAt(row, 4)
            t._val = delta
            t.setText(getFixedLenString(delta))
            t = self.layout.itemAt(row, 5)
            t._val = deltainv
            t.setText(getFixedLenString(deltainv))

    def addCursorCols(self):
        if self.expanded:
            return
        self.expanded = True
        if self.w0 is None:
            self.w0 = self.layout.geometry().width()

        self.layout.addItem(pg.LabelItem("C1"), 0, 2)
        self.layout.addItem(pg.LabelItem("C2"), 0, 3)
        self.layout.addItem(pg.LabelItem("Δ"), 0, 4)
        self.layout.addItem(pg.LabelItem("1/Δ"), 0, 5)

        for col in range(2, 6):
            self.layout.setColumnMaximumWidth(col, numValLen * 7)
            self.layout.setColumnMinimumWidth(col, numValLen * 7)

        if self.w1 is not None:
            self.setMaximumWidth(self.w1)

        for row in range(1, self.layout.rowCount()):
            for col in range(2, 6):
                item = pg.LabelItem("")
                item._val = None
                self.layout.addItem(item, row, col)

    def remCursorCols(self):
        if not self.expanded:
            return
        self.expanded = False
        if self.w1 is None:
            self.w1 = self.layout.geometry().width()

        self.layout.removeItem(self.layout.itemAt(0, 2))
        self.layout.removeItem(self.layout.itemAt(0, 3))
        self.layout.removeItem(self.layout.itemAt(0, 4))
        self.layout.removeItem(self.layout.itemAt(0, 5))

        for row in range(1, self.layout.rowCount()):
            for col in range(2, 6):
                self.layout.removeItem(self.layout.itemAt(row, col))

        if self.w0 is not None:
            self.setMaximumWidth(self.w0)

    def _addItemToLayout(self, sample, label):
        col = self.layout.columnCount()
        row = self.layout.rowCount()
        # in the original code, the next two lines are not commented out
        # if row:
        #    row -= 1
        # we need this bc we injected more rows and cols than in the original code
        if row == 2:
            col = 0
        else:
            col = 2

        nCol = self.columnCount * 2

        for col in range(0, nCol, 2):
            # FIND RIGHT COLUMN
            # if i dont add the row>=...,  get QGraphicsGridLayout::itemAt errors
            if row >= self.layout.rowCount() or not self.layout.itemAt(row, col):
                break

        self.layout.addItem(sample, row, col)
        self.layout.addItem(label, row, col + 1)
        # Keep rowCount in sync with the number of rows if items are added
        self.rowCount = max(self.rowCount, row + 1)
