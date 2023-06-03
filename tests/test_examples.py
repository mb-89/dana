from dana.examples import _browser


def test_examples(qtbot):
    win = _browser.Browser()
    win.show()
    qtbot.addWidget(win)
    for example in win.fileList:
        win.run(example)

    # edge-case:
    win.currentFile = None
    win.run()

    win.ui.files.selectionModel().clearSelection()

    win.ui.filter.setText("test")
    win.filt()
    win.filt(content=True)
