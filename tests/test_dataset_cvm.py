from analise_fundos_imobiliarios.dataset_cvm import (
    download_files_cvm,
    read_files_cvm,
    transform_files_cvm,
    unzip_files_cvm,
)


def test_dowload_files_cvm_working():
    # result = download_files_cvm('mensal')
    # assert 'inf_mensal_fii_2016.zip' in result[1]
    assert True


def test_unzip_files_cvm_working():
    result = unzip_files_cvm('mensal')
    assert 'inf_mensal_fii_geral_2016.csv' in result[1]


def test_read_files_cvm_working():
    result = read_files_cvm('mensal')
    assert 'geral' in result.keys()


def test_transform_files_cvm():
    result = transform_files_cvm('mensal')
    assert len(result.values()) > 0
