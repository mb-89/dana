import argparse

from . import __metadata__


def parseArgs(argv):
    p = argparse.ArgumentParser(
        prog=f"py -m {__metadata__.__projname__}.py",
        description=__metadata__.__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    p.add_argument("-v", "--version", action="store_true", help="prints version")

    p.add_argument(
        "path", type=str, help="path to the repo to analyze", default=None, nargs="?"
    )

    args = vars(p.parse_args(argv))
    return args, p


def main(argv=None):
    if not argv:
        argv = ["-h"]
    args, parser = parseArgs(argv)
    if args["version"]:
        print(__metadata__.__version__)
        return

    from . import api

    return 0
