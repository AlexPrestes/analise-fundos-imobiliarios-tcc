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
    return ts2g(ts)


@vectorize_metric
def number_of_nodes(graph: nx.Graph):
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


def distribution_degree(graph):
    list_degree = list(dict(nx.degree(graph)).values())
    x, y = np.histogram(
        list_degree,
        bins=nx.number_of_nodes(graph) + 1,
        range=(0, nx.number_of_nodes(graph) + 1),
    )
    y = y[:-1]

    return x, y


def coefficient_distribution_degree(graph):
    x, y = distribution_degree(graph)
    idx = x[2:] != 0
    fit = linregress(np.log(x[2:][idx]), np.log(y[2:][idx]))

    return fit
