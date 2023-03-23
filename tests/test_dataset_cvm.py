from analise_fundos_imobiliarios.dataset_cvm import DatasetFiiMensal


def test_datasetfiimensal_working():
    result = DatasetFiiMensal()
    result.run()
    assert result
