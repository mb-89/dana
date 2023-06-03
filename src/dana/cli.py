"""Provide a cli for all dana submodules."""

import argparse
import importlib.metadata as md


def main(argv):
    """Parse args and call requested functions."""
    metadata = md.metadata(__name__.split(".")[0])
    modname = metadata["Name"]
    parser = argparse.ArgumentParser(
        prog=modname,
        description=metadata["Summary"],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-v", "--version", action="store_true", help="prints version")
    kwargs = vars(parser.parse_args(argv))

    if kwargs["version"]:
        print(metadata["version"])
        return 0
