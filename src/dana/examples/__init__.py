"""Examples for dana."""
from pathlib import Path

from dana.examples._browser import show  # noqa: F401


def getExampleFiles():
    """Collect all files that contain example code."""
    p = Path(__file__)
    pp = p.parent
    files = {}
    for ex in pp.glob("**/*.py"):
        if ex.stem.startswith("_"):
            continue
        files[ex.stem] = ex
    return files


def runExample(name, code):
    """Run the given example code."""
    compiledCode = compile(code, name, "exec")
    glob = {}
    exec(compiledCode, glob)
    return glob
