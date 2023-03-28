import networkx as nx
import numpy as np
from scipy.stats import linregress
from ts2vg import NaturalVG


def time_series_to_visibility_graph(ts):
    return NaturalVG(directed=None).build(ts.flatten()).as_networkx()


def time_series_to_metric(ts, metric):
    graph = time_series_to_visibility_graph(ts)
    return metric(graph)


time_series_to_metric = np.vectorize(
    time_series_to_metric,
    otypes=[np.float32],
    signature='(i),()->()',
)


def number_of_nodes(graph):
    return graph.number_of_nodes()


def average_clustering(graph):
    if number_of_nodes(graph):
        return nx.average_clustering(graph)
    else:
        return 0


def average_short_path(graph):
    if number_of_nodes(graph):
        return nx.average_shortest_path_length(graph)
    else:
        return 0


def density(graph):
    if number_of_nodes(graph):
        return nx.density(graph)
    else:
        return 0


def number_of_edges(graph):
    if number_of_nodes(graph):
        return graph.number_of_edges()
    else:
        return 0


def average_degree(graph):
    if number_of_nodes(graph):
        return np.mean(list(dict(nx.degree(graph)).values()))
    else:
        return 0


def distribution_degree(graph):
    list_degree = list(dict(nx.degree(graph)).values())
    x, y = np.histogram(
        list_degree,
        bins=graph.number_of_nodes() + 1,
        range=(0, graph.number_of_nodes() + 1),
    )
    y = y[:-1]

    return x, y


def coefficient_distribution_degree(graph):
    x, y = distribution_degree(graph)
    idx = x[2:] != 0
    fit = linregress(np.log(x[2:][idx]), np.log(y[2:][idx]))

    return fit
