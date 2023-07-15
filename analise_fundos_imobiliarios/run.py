from analise_fundos_imobiliarios.analytics import *


def run_treino():
    ds_treino = Dataset(n=100, L0=10, L=82)
    ds_treino.run()
    ds_treino.to_netcdf('dataset/treino/dataset_treino_series.nc')
    ds_treino_metrica = dataarray_metrics(ds_treino)
    ds_treino_metrica = ds_treino_metrica.merge(ds_treino.target)
    ds_treino_metrica.to_netcdf('dataset/treino/dataset_treino_metrica_series.nc')

    del ds_treino_metrica

    ds_treino_metrica = dataarray_metrics(ds_treino, diff=True)
    ds_treino_metrica = ds_treino_metrica.merge(ds_treino.target)
    ds_treino_metrica.to_netcdf('dataset/treino/dataset_treino_metrica_series_diff.nc')

    del ds_treino
    del ds_treino_metrica


def run_fii_mensal():
    ds_fii = transform_files_cvm_mensal()
    ds_fii_metrica, df_cat = metrics_fii_mensal(ds_fii)
    ds_fii_metrica.to_netcdf('dataset/cvm/dataset_cvm_metrica_mensal.nc')
    df_cat.to_csv('dataset/cvm/dataset_cvm_metrica_mensal_dados.csv')
