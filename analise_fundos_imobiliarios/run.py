from analise_fundos_imobiliarios.analytics import *


def run_fii_mensal():
    ds_fii = transform_files_cvm_mensal()
    ds_fii_metrica, df_cat = metrics_fii_mensal(ds_fii)
    ds_fii_metrica.to_netcdf('dataset/cvm/dataset_cvm_metrica_mensal.nc')
    df_cat.to_csv('dataset/cvm/dataset_cvm_metrica_mensal_dados.csv')
