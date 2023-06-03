import pandas as pd

import dana  # noqa: F401


def test_hook():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
    df.plot(backend="dana")
