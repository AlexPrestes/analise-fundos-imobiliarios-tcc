from analise_fundos_imobiliarios.dataset_cvm import DatasetFiiMensal


def test_datasetfiimensal_working():
    dataset = DatasetFiiMensal()
    dataset.run()
    result = dataset.data
    assert result
