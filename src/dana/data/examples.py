import itertools as itt
from math import sqrt

import numpy as np
import pandas as pd
from scipy import signal


def getExampleData(key):
    yield from examplegallery.get(
        key.replace("#example", "").strip("_"), createStepresponses
    )()


def createStepresponses():
    omegas = np.linspace(1, 10, 10)
    zetas = np.linspace(0, 2, 10)
    params = tuple(itt.product(omegas, zetas))

    for idx, (omega, zeta) in enumerate(params):
        yield f"df{idx}", createStepresponse(omega, zeta)


examplegallery = {"stepresponses": createStepresponses}


def createStepresponse(omega, zeta):
    df = pd.DataFrame()

    # using the formulas from
    # https://electronics.stackexchange.com/questions/296567/over-and-critically-damped-systems-settling-time
    # we can estimate the settling time without calculating the complete stepresponse
    metadata = {"omega": omega, "zeta": zeta}
    match omega:
        case _ if zeta == 0:
            ts = float("inf")
        case _ if zeta < 1:
            ts = 3.91 / (omega * zeta)
        case _ if zeta == 1:
            ts = 5.8335 / omega
        case _ if zeta > 1:
            ts = 3.172 / (omega * sqrt(zeta**2 - 1))
    metadata["ts"] = ts

    num = [1]
    denom = [1 / (omega**2), 2 * zeta / omega, 1]
    lti = signal.lti(num, denom)
    t, y = signal.step(lti)

    df["time"] = t
    df["y1"] = y
    df.set_index("time", inplace=True)

    df.attrs = metadata
    return df
