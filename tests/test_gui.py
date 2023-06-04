import pandas as pd

from dana.examples import _browser


def test_examples(qtbot):

    win = _browser.Browser()
    win.show()
    qtbot.addWidget(win)
    #we need to store the qt objects,
    #else they get destroyed immediately
    objects = [] 
    for example in win.fileList:
        objects.append(win.run(example))


    # edge-case:
    win.currentFile = None
    objects.append(win.run())

    win.ui.files.selectionModel().clearSelection()

    win.ui.filter.setText("test")
    win.filt()
    win.filt(content=True)
    qtbot.wait(100)

def test_edgecases(qtbot):

    df = pd.DataFrame()
    p1 = df.plot(backend="dana")
    df["x"] = [0, 1, 2]
    p2 = df.plot(backend="dana", plugins=[])
    p3 = df.plot(backend="dana", kind="barh")