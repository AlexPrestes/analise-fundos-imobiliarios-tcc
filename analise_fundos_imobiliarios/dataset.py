import numpy as np
import xarray as xr

from analise_fundos_imobiliarios.series import (
    fbm_negative,
    fbm_none,
    fbm_positive,
    logistic_map,
    random,
    sine_map,
)


class Dataset(xr.Dataset):
    __slots__ = ('n', 'L0', 'L', 'list_series')

    def __init__(self, n=20, L0=10, L=60):
        super().__init__()
        self.n = n
        self.L0 = L0
        self.L = L + 1
        self.list_series = [
            fbm_negative,
            fbm_none,
            fbm_positive,
            logistic_map,
            random,
            sine_map,
        ]

    def run(self):
        n = len(self.list_series) * self.n * (self.L - self.L0)
        m = self.L
        shape_data = (n, m)
        list_features = np.empty(shape_data, dtype=np.float32)
        list_target = []
        ts_fill = np.empty((m,))
        ts_fill.fill(np.nan)
        line_i = 0

        for i in range(self.L0, self.L):
            for _ in range(self.n):
                for func in self.list_series:
                    ts = func(i)
                    list_features[line_i, :] = np.append(ts, ts_fill[i:])
                    list_target.append(str(func.__qualname__))
                    line_i += 1

        data = xr.DataArray(
            data=list_features,
            dims=['id', 'time'],
            coords=[range(n), range(m)],
        )

        target = xr.DataArray(
            data=list_target,
            dims='id',
            coords=[range(n)],
        )

        super().__init__(data_vars=dict(series=data, target=target))

    def set_series(self, series=[logistic_map, fbm_positive]):
        self.list_series = series
