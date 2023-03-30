import networkx as nx
import numpy as np


def vectorize_metric(func):
    def inner1(*args, **kwargs):
        if isinstance(args[0], nx.Graph):
            return func(*args, **kwargs)
        else:
            return np.vectorize(func, signature='()->()')(*args, **kwargs)

    return inner1
