from analise_fundos_imobiliarios.analytics import *


def test_metrics_fii_mensal_working():
    ds_fii = transform_files_cvm_mensal()
    ds_fii_metrica, df_cat = metrics_fii_mensal(
        ds_fii.sel(CNPJ_Fundo=ds_fii.Acoes.CNPJ_Fundo.values[:5])
    )
    print('aew', ds_fii_metrica.size, df_cat.size, 'asdasd')
    assert ds_fii_metrica.shape and df_cat.shape
