"""Analyzes and plots data."""


def plot(data, kind, **kwargs):
    """Provide an entry point for pandas.

    | Can be executed via:
    | import dana
    | import pandas as pd
    | pd.DataFrame().plot(backend="dana").

    We add the entry point dynamically, so it also works in editable mode:
    https://stackoverflow.com/a/48666503
    """
    data.plot(backend="matplotlib", kind=kind, **kwargs)


def _addEntryPoint():
    """Register the pandas entry point on import."""
    import pkg_resources

    d = pkg_resources.Distribution(__file__)
    ep = pkg_resources.EntryPoint.parse("dana = dana:plot", dist=d)
    d._ep_map = {"pandas_plotting_backends": {"dana": ep}}
    pkg_resources.working_set.add(d, "dana")


_addEntryPoint()
