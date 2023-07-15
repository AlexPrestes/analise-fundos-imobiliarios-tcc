import networkx as nx
import numpy as np
import pandas as pd
from pyxirr import xirr


def vectorize_metric(func):
    def inner1(*args, **kwargs):
        if isinstance(args[0], nx.Graph):
            return func(*args, **kwargs)
        else:
            return np.vectorize(func, signature='()->()')(*args, **kwargs)

    return inner1


def aumento_patrimonial_fundo(ds, cnpj_fundo):
    da = ds.sel(CNPJ_Fundo=cnpj_fundo)['Valor_Patrimonial_Cotas'].dropna('Data_Referencia')
    da = da/da.shift(Data_Referencia=1)
    da = da*(1-ds.sel(CNPJ_Fundo=cnpj_fundo)['Percentual_Amortizacao_Cotas_Mes'].shift(Data_Referencia=1))
    da = np.round(da, 2)
    da[da == np.inf] = np.nan
    da[da == 0.] = np.nan
    da = da.fillna(1.)
    da.name = 'Valor_Patrimonial_Cotas'

    dc = ds.sel(CNPJ_Fundo=cnpj_fundo)['Cotas_Emitidas'].dropna('Data_Referencia')
    dc = dc/dc.shift(Data_Referencia=1)
    dc = np.round(dc, 2)
    dc[dc == np.inf] = np.nan
    dc[dc == 0.] = np.nan
    dc = dc.fillna(1.)

    dp = ds.sel(CNPJ_Fundo=cnpj_fundo)['Patrimonio_Liquido'].dropna('Data_Referencia')
    dk = dp.copy()
    dp = dp/dp.shift(Data_Referencia=1)
    dp = np.round(dp, 2)
    dp[dp == np.inf] = np.nan
    dp[dp == 0.] = np.nan
    dp = dp.fillna(1.)

    da_result = da.copy()

    for n, i, j, k in zip(range(len(dc.values)), dc.values, da.values, dp.values):
        da_result[n] = np.nan
        #  Primeira Verificação
        #  Aumento do número de cotas
        #  Pode ser 2 situações
        #
        #  Desdobramento: aumenta as cotas
        #                 diminui o valor patrimonial por cota
        #                 mantém o patrimonio liquido
        #
        #  Emissão: aumenta as cotas
        #           mantém o valor patrimonial por cota
        #           aumenta o patrimonio liquido
        if i > 1. and k >= j:
            da_result[n] = dk.values[n]-dk.values[n-1]

    da_result = da_result.to_dataframe().drop(columns=['CNPJ_Fundo']).dropna()
    da_result = da_result.rename(columns={'Valor_Patrimonial_Cotas': 'FC'})

    return da_result


def fluxo_caixa_fundo(ds, cnpj_fundo):
    #  Entradas
    ##  Dividend Yield

    df_dy = -ds.sel(CNPJ_Fundo=cnpj_fundo)['Percentual_Dividend_Yield_Mes']
    df_dy *= ds.sel(CNPJ_Fundo=cnpj_fundo)['Patrimonio_Liquido'].shift(Data_Referencia=-1)
    df_dy[df_dy == 0] = np.nan
    df_dy = df_dy.to_dataframe().drop(columns=['CNPJ_Fundo']).dropna()
    df_dy = df_dy.rename(columns={'Percentual_Dividend_Yield_Mes': 'FC'})

    df_amor = -ds.sel(CNPJ_Fundo=cnpj_fundo)['Percentual_Amortizacao_Cotas_Mes']
    df_amor *= ds.sel(CNPJ_Fundo=cnpj_fundo)['Patrimonio_Liquido'].shift(Data_Referencia=-1)
    df_amor[df_amor == 0] = np.nan
    df_amor = df_amor.to_dataframe().drop(columns=['CNPJ_Fundo']).dropna()
    df_amor = df_amor.rename(columns={'Percentual_Amortizacao_Cotas_Mes': 'FC'})
    
    df_fc_di = ds.sel(CNPJ_Fundo=cnpj_fundo)['Patrimonio_Liquido']
    df_fc_di = df_fc_di.dropna('Data_Referencia')[[0, -1]]
    df_fc_di[1] *= -1
    df_fc_di = df_fc_di.to_dataframe().drop(columns=['CNPJ_Fundo'])
    df_fc_di = df_fc_di.rename(columns={'Patrimonio_Liquido': 'FC'})

    df_emiss = aumento_patrimonial_fundo(ds, cnpj_fundo)

    df_fc = pd.concat([df_fc_di, df_dy, df_amor, df_emiss], axis=0).sort_values('Data_Referencia')

    return df_fc


def tir_fundo(ds, cnpj_fundo):
    try:
        fc_fundo = fluxo_caixa_fundo(ds, cnpj_fundo)
        fc_dates = fc_fundo.index.values
        fc_values = fc_fundo.values.flatten()
        tir = xirr(fc_dates, fc_values)
    except:
        tir = np.nan

    return tir
