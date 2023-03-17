from analise_fundos_imobiliarios.metrics import *
from analise_fundos_imobiliarios.series import logistic_map


def test_time_series_to_visibility_graph_working():
    ts = logistic_map(20)
    result = time_series_to_visibility_graph(ts)
    assert result


def test_number_of_nodes_working():
    ts = logistic_map(20)
    vg = time_series_to_visibility_graph(ts)
    result = number_of_nodes(vg)
    assert result


def test_average_clustering_working():
    ts = logistic_map(20)
    vg = time_series_to_visibility_graph(ts)
    result = average_clustering(vg)
    assert result


def test_average_clustering_empty_working():
    ts = logistic_map(1)
    vg = time_series_to_visibility_graph(ts)
    result = average_clustering(vg)
    assert result == 0


def test_average_short_path_working():
    ts = logistic_map(20)
    vg = time_series_to_visibility_graph(ts)
    result = average_short_path(vg)
    assert result


def test_average_short_path_empty_working():
    ts = logistic_map(1)
    vg = time_series_to_visibility_graph(ts)
    result = average_short_path(vg)
    assert result == 0


def test_density_working():
    ts = logistic_map(20)
    vg = time_series_to_visibility_graph(ts)
    result = density(vg)
    assert result


def test_density_empty_working():
    ts = logistic_map(1)
    vg = time_series_to_visibility_graph(ts)
    result = density(vg)
    assert result == 0


def test_number_of_edges_working():
    ts = logistic_map(20)
    vg = time_series_to_visibility_graph(ts)
    result = number_of_edges(vg)
    assert result


def test_number_of_edges_empty_working():
    ts = logistic_map(1)
    vg = time_series_to_visibility_graph(ts)
    result = number_of_edges(vg)
    assert result == 0


def test_average_degree_working():
    ts = logistic_map(20)
    vg = time_series_to_visibility_graph(ts)
    result = average_degree(vg)
    assert result


def test_average_degree_empty_working():
    ts = logistic_map(1)
    vg = time_series_to_visibility_graph(ts)
    result = average_degree(vg)
    assert result == 0


def test_distribution_degree_working():
    ts = logistic_map(20)
    vg = time_series_to_visibility_graph(ts)
    result = distribution_degree(vg)
    assert len(result) == 2


def test_coefficient_distribution_degree_working():
    ts = logistic_map(20)
    vg = time_series_to_visibility_graph(ts)
    result = coefficient_distribution_degree(vg)
    assert result


def test_time_series_to_metrics_working():
    ts = logistic_map(1000)
    result = time_series_to_metrics(
        ts, [average_clustering, density, coefficient_distribution_degree]
    )
    assert len(result) == 3
