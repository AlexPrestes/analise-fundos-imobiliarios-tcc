from analise_fundos_imobiliarios.dataset_cvm import DatasetCVM


def test_datasetcvm_working():
    result = DatasetCVM()
    assert result


def test_datasetcvm_set_columns_series_working():
    result = DatasetCVM()
    result.columns_series(['Valor_Ativo', 'Patrimonio_Liquido'])
    assert result.list_columns_series == ['Valor_Ativo', 'Patrimonio_Liquido']


def test_datasetcvm_columns_series_working():
    result = DatasetCVM()
    result.columns_series()
    assert len(result.list_columns_series) == 55


def test_datasetcvm_run_working():
    result = DatasetCVM('mensal', [2016, 2016])
    result.run()
    assert result.data.shape == (150, 55)
