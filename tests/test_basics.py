from dana import cli


def test_cli():
    assert cli.main(["-v"]) == 0
