import numpy as np
import pandas as pd

from analise_fundos_imobiliarios.series import (
    fbm_negative,
    fbm_none,
    fbm_positive,
    logistic_map,
    random,
    sine_map,
)


class Dataset:
    def __init__(self, n=20, L0=10, L=60):
        self.n = n
        self.L0 = L0
        self.L = L
        self.list_series = [
            fbm_negative,
            fbm_none,
            fbm_positive,
            logistic_map,
            random,
            sine_map,
        ]

    def run(self):
        list_features = []
        list_target = []

        for i in range(self.L0, self.L):
            for _ in range(self.n):
                for func in self.list_series:
                    ts = func(i)
                    list_features.append(ts)
                    list_target.append(str(func.__qualname__))

        self.data = pd.DataFrame(
            pd.Series(list_features), columns=['time_series']
        )
        self.data['target'] = pd.Series(list_target)

    def set_series(self, series=[logistic_map, fbm_positive]):
        self.list_series = series
