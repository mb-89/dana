from dana.examples import _browser


def test_cli(qtbot):
    win = _browser.Browser()
    win.show()
    qtbot.addWidget(win)
    for example in win.fileList:
        win.run(example)
