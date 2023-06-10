import tempfile
from pathlib import Path

import pandas as pd
from dtreeviz.utils import DTreeVizRender

from dana.examples import _browser


def test_examples(qtbot, monkeypatch):
    win = _browser.Browser()
    win.show()
    qtbot.addWidget(win)
    # we need to store the qt objects,
    # else they get destroyed immediately
    objects = []
    with tempfile.TemporaryDirectory() as td:
        htmlf = Path(td) / "tmp.svg"
        open(htmlf, "w").write("")

        def mockSVG(*args, **kwargs):
            return htmlf

        with monkeypatch.context() as m:
            m.setattr(DTreeVizRender, "save_svg", mockSVG)
            for example in win.fileList:
                objects.append(win.run(example.data(_browser.DATA.PATH.value)))

    # edge-case:
    win.currentFile = None
    objects.append(win.run())

    win.ui.files.selectionModel().clearSelection()

    win.ui.filter.setText("test")
    win.filt()
    win.filt(content=True)
    qtbot.wait(100)


def test_edgecases_general(qtbot):
    df = pd.DataFrame()
    p1 = df.plot(backend="dana")  # noqa: F841
    df["x"] = [0, 1, 2]
    p2 = df.plot(backend="dana", plugins=[])  # noqa: F841
    p3 = df.plot(backend="dana", kind="barh")  # noqa: F841


def test_edgecases_decisiontree(qtbot):
    from dana.decisiontree import widgets

    b = widgets.PlotBuilder()
    b.setSrc(None, "name")


def test_cli_plot(qtbot):
    from dana import cli

    cli.main(["df_sincos"], exec=False)
    cli.main(["df_sincos.invalid"], exec=False)
