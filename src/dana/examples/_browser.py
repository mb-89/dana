"""Browser for dana examples."""

from enum import Enum
from pathlib import Path

import pyqtgraph as pg
from pyqtgraph.examples.ExampleApp import PythonHighlighter
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets


class DATA(Enum):
    """Data shorthands used to store stuff in qt items."""

    USERROLE = QtCore.Qt.UserRole
    PATH = QtCore.Qt.UserRole + 1


class FILTMODE(Enum):
    """Options for the example filters."""

    FILENAME = 1
    FILECONTENT = 2


def show():  # pragma: no cover: browser is tested completely in test_examples
    """Show the example browser."""
    pg.mkQApp()

    b = Browser()

    b.resize(1000, 500)
    b.show()
    b.ui.splitter.setSizes([250, 750])

    pg.exec()


class Browser(QtWidgets.QMainWindow):
    """Browser for dana examples.

    This class is heavily (!) inspired from pyqtgraph.examples.
    """

    def __init__(self) -> None:
        """Instanciate the browser."""
        super().__init__()
        self.ui = Browser_template()
        self.cw = QtWidgets.QWidget()
        self.setCentralWidget(self.cw)
        self.ui.setupUi(self.cw)
        self.setWindowTitle("Dana Examples")
        self.currentFile = None

        self.fileList = self.loadFiles()

        self.hl = PythonHighlighter(self.ui.code.document())

        self.action_run_sc = QtGui.QShortcut(QtGui.QKeySequence("F5"), self)
        self.action_run_sc.activated.connect(self.run)
        self.ui.runButton.clicked.connect(self.run)

        self.action_filt_sc = QtGui.QShortcut(QtGui.QKeySequence("F2"), self)
        self.action_filt_sc.activated.connect(self.filt)
        self.action_filt_sc = QtGui.QShortcut(QtGui.QKeySequence("F3"), self)
        self.action_filt_sc.activated.connect(lambda: self.filt(content=True))

        self._buf = {}

    def run(self, file=None):
        """Run the given example (or the currently opened one)."""
        if file is None:
            file = self.currentFile
        if file is None:
            return
        edittxt = self.ui.code.toPlainText()
        from dana.examples import runExample

        results = runExample(self.currentFile.name, edittxt)
        self._buf = results
        return results

    def filt(self, content=False):
        """Filter Example list by name or content."""
        filt = self.ui.filter.text()
        mdl = self.ui.files.model()
        mdl._mode = FILTMODE.FILECONTENT if content else FILTMODE.FILENAME
        self.hl.searchText = filt if FILTMODE.FILECONTENT else None
        mdl.setFilterRegularExpression(filt)
        mdl.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

    def loadFiles(self):
        """Load all example files into the list in the GUI."""
        from dana.examples import getExampleFiles

        mdl = QtGui.QStandardItemModel()
        root = mdl.invisibleRootItem()
        p = Path(__file__)
        pp = p.parent
        items = {}
        fileItems = []
        exampledict = getExampleFiles()
        for ex in exampledict.values():
            pr = ex.relative_to(pp)
            parents = tuple(reversed(pr.parents))[1:]
            parentItem = items.get(parents)
            if parentItem is None:
                if not parents:
                    parentItem = root
                else:  # pragma: no cover / only needed once we have nested examples
                    grandparent = items.get(parents[:-1])
                    parentItem = QtGui.QStandardItem(str(parents[-1].stem))
                    parentItem.setEditable(False)
                    grandparent.appendRow([parentItem])
                items[parents] = parentItem

            item = QtGui.QStandardItem(str(ex.name))
            item.setData(ex, DATA.PATH.value)
            item.setEditable(False)
            parentItem.appendRow([item])
            fileItems.append(item)

        proxyMdl = TreeMdl()
        proxyMdl.setSourceModel(mdl)

        self.ui.files.setModel(proxyMdl)
        self.ui.files.expandAll()
        self.ui.files.selectionModel().selectionChanged.connect(self.showFile)
        self.ui.files.selectionModel().select(
            fileItems[0].index(), QtCore.QItemSelectionModel.Select
        )

        return fileItems

    def showFile(self):
        """Show the content of the current file in the GUI."""
        self.currentFile = None
        self.ui.code.setPlainText("")
        self.ui.fileLabel.setText("")
        selectedIDX = self.ui.files.selectedIndexes()
        if len(selectedIDX) < 1:
            return
        else:
            selectedIDX = selectedIDX[0]

        fn = selectedIDX.data(DATA.PATH.value)
        if fn is None or not fn.is_file():  # pragma: no cover: generic edge-case
            return
        self.currentFile = fn
        self.ui.code.setPlainText(open(fn, "r").read())
        self.ui.fileLabel.setText(" " + str(fn))


class TreeMdl(QtCore.QSortFilterProxyModel):
    """A Tree that allows for filtering by name and content."""

    def __init__(self):
        super().__init__()
        self.setRecursiveFilteringEnabled(True)
        self._mode = FILTMODE.FILENAME

    def filterAcceptsRow(self, row, parent):
        """Return true if the element is accepted by the filter, else false."""
        if self._mode == FILTMODE.FILENAME:
            return super().filterAcceptsRow(row, parent)

        sm = self.sourceModel()
        fn = sm.index(row, 0, parent).data(DATA.PATH.value)
        if fn is None or not fn.is_file():  # pragma: no cover / edge case for empty nodes/files
            return False

        txt = open(fn, "r").read()
        return self.filterRegularExpression().globalMatch(txt).hasNext()


class Browser_template(object):
    """Template for browser guis."""

    def setupUi(self, Form):
        """Create all ui elements."""
        Form.setObjectName("Form")
        self.rootLayout = QtWidgets.QGridLayout(Form)
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.rootLayout.setSpacing(0)
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)

        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.browserLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.browserLayout.setContentsMargins(0, 0, 0, 0)
        self.browserLayout.setSpacing(0)
        self.filter = QtWidgets.QLineEdit()
        self.filter.setPlaceholderText("Filter / F2: filter by title / F3: filter by content")
        self.browserLayout.addWidget(self.filter)
        self.files = QtWidgets.QTreeView()
        self.files.header().setVisible(False)
        self.files.setAlternatingRowColors(True)
        self.browserLayout.addWidget(self.files)

        self.layoutWidget2 = QtWidgets.QWidget(self.splitter)
        self.codeLayout = QtWidgets.QGridLayout(self.layoutWidget2)
        self.codeLayout.setContentsMargins(0, 0, 0, 0)
        self.codeLayout.setSpacing(0)
        self.runButton = QtWidgets.QPushButton("Run / F5")
        self.fileLabel = QtWidgets.QLabel("")
        font = QtGui.QFont()
        font.setBold(True)
        self.fileLabel.setFont(font)
        self.fileLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.runButton.setMaximumWidth(150)
        self.codeLayout.addWidget(self.runButton, 0, 0)
        self.codeLayout.addWidget(self.fileLabel, 0, 1, 1, 2)

        self.code = QtWidgets.QPlainTextEdit()
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.code.setFont(font)
        self.codeLayout.addWidget(self.code, 1, 0, 1, 3)

        self.rootLayout.addWidget(self.splitter)
