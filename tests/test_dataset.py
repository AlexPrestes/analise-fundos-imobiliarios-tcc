from analise_fundos_imobiliarios.dataset import Dataset
from analise_fundos_imobiliarios.series import fbm_positive, logistic_map


def test_dataset_working():
    result = Dataset()
    assert result


def test_dataset_set_series_working():
    result = Dataset()
    result.set_series([fbm_positive, logistic_map])
    assert result


def test_dataset_run_working():
    result = Dataset(n=4, L0=2, L=5)
    result.run()
    assert result.data.size == 72
