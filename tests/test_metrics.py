from random import random

from analise_fundos_imobiliarios.metrics import *

seq_random = lambda n: np.asarray([random() for _ in range(n)])


def test_time_series_to_visibility_graph_working():
    ts = seq_random(20)
    result = time_series_to_visibility_graph(ts)
    assert result


def test_number_of_nodes_working():
    ts = seq_random(20)
    vg = time_series_to_visibility_graph(ts)
    result = number_of_nodes(vg)
    assert result


def test_average_clustering_working():
    ts = seq_random(20)
    vg = time_series_to_visibility_graph(ts)
    result = average_clustering(vg)
    assert result


def test_average_clustering_empty_working():
    ts = seq_random(0)
    vg = time_series_to_visibility_graph(ts)
    result = average_clustering(vg)
    assert result == 0


def test_average_short_path_working():
    ts = seq_random(20)
    vg = time_series_to_visibility_graph(ts)
    result = average_short_path(vg)
    assert result


def test_average_short_path_empty_working():
    ts = seq_random(1)
    vg = time_series_to_visibility_graph(ts)
    result = average_short_path(vg)
    assert result == 0


def test_density_working():
    ts = seq_random(20)
    vg = time_series_to_visibility_graph(ts)
    result = density(vg)
    assert result


def test_density_empty_working():
    ts = seq_random(1)
    vg = time_series_to_visibility_graph(ts)
    result = density(vg)
    assert result == 0


def test_number_of_edges_working():
    ts = seq_random(20)
    vg = time_series_to_visibility_graph(ts)
    result = number_of_edges(vg)
    assert result


def test_number_of_edges_empty_working():
    ts = seq_random(1)
    vg = time_series_to_visibility_graph(ts)
    result = number_of_edges(vg)
    assert result == 0


def test_average_degree_working():
    ts = seq_random(20)
    vg = time_series_to_visibility_graph(ts)
    result = average_degree(vg)
    assert result


def test_average_degree_empty_working():
    ts = seq_random(1)
    vg = time_series_to_visibility_graph(ts)
    result = average_degree(vg)
    assert result == 0


def test_coefficient_distribution_degree_working():
    ts = seq_random(20)
    vg = time_series_to_visibility_graph(ts)
    result = coefficient_distribution_degree(vg)
    assert result


def test_coefficient_distribution_degree_empty_working():
    ts = seq_random(0)
    vg = time_series_to_visibility_graph(ts)
    result = coefficient_distribution_degree(vg)
    assert result
