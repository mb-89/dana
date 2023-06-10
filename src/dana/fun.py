"""Generic functions used in many places."""

import inspect


def callWithKnownArgs(fn, argdct):
    """Call the given function with all kwargs that is accepts from the given dict."""
    sig = inspect.signature(fn)
    allowedArgs = [
        param.name
        for param in sig.parameters.values()
        if param.kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY)
    ]
    argdct = dict((k, v) for k, v in argdct.items() if k in allowedArgs)

    return fn(**argdct)
