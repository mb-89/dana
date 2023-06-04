import os

import pytest
from pyqtgraph import Qt


def pytest_configure(config):
    # force qtbot to use the same backend as pyqtgraph
    os.environ["PYTEST_QT_API"] = Qt.QT_LIB.lower()


@pytest.fixture(scope="session")
def qapp():
    yield Qt.mkQApp()
