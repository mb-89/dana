"""Provide a cli for all dana submodules."""

import argparse
import importlib.metadata as md


def main(argv):
    """Parse args and call requested functions."""
    parser = mkparser()
    args = vars(parser.parse_args(argv))

    if args["version"]:
        print(parser._moduleversion)
        return 0

    if args["examples"]:  # pragma: no cover / tested explicitely in tests_examples
        import dana
        import dana.examples

        examples = dana.examples.getExampleFiles()
        if args["src"] in examples:
            name = args["src"]
            code = open(examples[name], "r").read()
            _ = dana.examples.runExample(name, code)
            dana.exec()
        else:
            dana.examples.show()
            return 0


def mkparser(parser=None):
    """Create a parser we can use to parse arguments.

    In case we pass an existing parser, the args get appended to it.
    """
    if parser is None:
        metadata = md.metadata(__name__.split(".")[0])
        modname = metadata["Name"]
        parser = argparse.ArgumentParser(
            prog=modname,
            description=metadata["Summary"],
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    parser._moduleversion = metadata["version"]

    parser.add_argument("src", nargs="?", default=None, help="source, if given")
    parser.add_argument("-v", "--version", action="store_true", help="prints version")
    parser.add_argument("--examples", action="store_true", help="shows example browser")

    return parser
