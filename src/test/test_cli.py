import webbrowser
from pathlib import Path

import pytest

cli = pytest.module_cli


def noop(*args, **kwargs):
    pass


def test_main(monkeypatch):
    assert cli.main(["-v"]) is None

    with pytest.raises(SystemExit) as e:
        cli.main(["-h"])
        assert e.type == SystemExit

    with monkeypatch.context() as m:
        m.setattr(webbrowser, "open", noop)
        assert cli.main([str(Path(__file__).parent.parent.parent)]) == 0

    with pytest.raises(SystemExit) as e:
        cli.main()
        assert e.type == SystemExit
