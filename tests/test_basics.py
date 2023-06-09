from dana import cli


def test_cli():
    assert cli.main(["-v"]) == 0


def test_cli_edcases():
    assert cli.main(["--args", "test"]) == -1
    assert cli.main(["--args", "test", "test"]) == 0
