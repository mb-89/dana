import pytest

from dana import cli


def pytest_configure():
    pytest.module_cli = cli
