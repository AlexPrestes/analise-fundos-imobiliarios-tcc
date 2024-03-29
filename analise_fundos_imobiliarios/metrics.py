import networkx as nx
import numpy as np
from scipy.stats import linregress
from ts2vg import NaturalVG

from analise_fundos_imobiliarios.utils import vectorize_metric


def time_series_to_visibility_graph(ts):
    ts2g = np.vectorize(
        lambda x: NaturalVG(directed=None).build(x).as_networkx(),
        otypes=[nx.Graph],
        signature='(i)->()',
    )
    return ts2g(np.asarray(ts, dtype=np.float32))


@vectorize_metric
def number_of_nodes(graph):
    return nx.number_of_nodes(graph)


@vectorize_metric
def average_clustering(graph):
    if nx.number_of_nodes(graph):
        return nx.average_clustering(graph)
    else:
        return 0


@vectorize_metric
def average_short_path(graph):
    if nx.number_of_nodes(graph):
        return nx.average_shortest_path_length(graph)
    else:
        return 0


@vectorize_metric
def density(graph):
    if nx.number_of_nodes(graph):
        return nx.density(graph)
    else:
        return 0


@vectorize_metric
def number_of_edges(graph):
    return nx.number_of_edges(graph)


@vectorize_metric
def average_degree(graph):
    if nx.number_of_nodes(graph):
        return np.mean(list(dict(nx.degree(graph)).values()))
    else:
        return 0


@vectorize_metric
def coefficient_distribution_degree(graph):
    list_degree = list(dict(graph.degree()).values())
    x, y = np.histogram(
        list_degree,
        bins=nx.number_of_nodes(graph) + 1,
        range=(0, nx.number_of_nodes(graph) + 1),
    )
    y = y[:-1]
    idx = y[2:] != 0
    try:
        fit = linregress(np.log(x[2:][idx]), np.log(y[2:][idx])).slope
    except:
        fit = np.nan

    return fit
