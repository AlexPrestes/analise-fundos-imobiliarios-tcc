import numpy as np
from fbm import fbm
from numpy._typing import NDArray


def logistic_map(n: int = 2, r: float = 4.0) -> NDArray:
    """
    Gera uma série temporal do mapa logistico

    Parameters:
        n: Comprimento da série
        r: Taxa de crescimento

    Returns:
        Uma lista com os valores da série

    """
    x_serie = np.zeros(n)
    x_serie[0] = np.random.random()

    for i in range(1, n):
        x_serie[i] = r * x_serie[i - 1] * (1 - x_serie[i - 1])
    return x_serie


def sine_map(n: int = 2, r: float = 1.0) -> NDArray:
    x_serie = np.zeros(n)
    x_serie[0] = np.random.random()

    for i in range(1, n):
        x_serie[i] = r * np.sin(np.pi * x_serie[i - 1])
    return x_serie


def fbm_positive(n: int = 2, hurst: float = 0.7) -> NDArray:
    return fbm(n=(n - 1), hurst=hurst)


def fbm_negative(n: int = 2, hurst: float = 0.2) -> NDArray:
    return fbm(n=(n - 1), hurst=hurst)


def fbm_none(n: int = 2, hurst: float = 0.5) -> NDArray:
    return fbm(n=(n - 1), hurst=hurst)


def random(n: int) -> NDArray:
    return np.random.random(n)
