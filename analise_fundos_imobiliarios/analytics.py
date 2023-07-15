from operator import index
import warnings

from analise_fundos_imobiliarios.dataset import *
from analise_fundos_imobiliarios.dataset_cvm import *
from analise_fundos_imobiliarios.metrics import *
from analise_fundos_imobiliarios.utils import *

warnings.filterwarnings('ignore')


def dataarray_metrics(
    ds, variable='series', input_core_dims='time', metrics=None, diff=False
):
    if metrics == None:
        metrics = [
            'average_clustering',
            'average_degree',
            'average_short_path',
            'coefficient_distribution_degree',
            'density',
            'number_of_edges',
            'number_of_nodes',
        ]
    metrics = np.asarray(metrics)

    ds_serie = ds[variable]

    if diff:
        ds_serie = ds[variable].diff(dim=input_core_dims)

    da_vg = xr.apply_ufunc(
        time_series_to_visibility_graph,
        ds_serie,
        input_core_dims=[[input_core_dims]],
    )

    metrics_vg = [eval(func)(da_vg) for func in metrics]
    metrics_vg = np.asarray(metrics_vg)
    metrics_vg = xr.DataArray(
        metrics_vg,
        dims=('metrica', da_vg.dims[0]),
        coords={
            da_vg.dims[0]: da_vg.coords[da_vg.dims[0]],
            'metrica': metrics,
        },
    )

    return xr.Dataset({variable: metrics_vg})


def metrics_fii_mensal(ds, diff=False):
    variables = ds.to_array().coords['variable'].values
    ds_out = dataarray_metrics(ds, variables[0], 'Data_Referencia', diff=diff)
    df_string = None

    for var in variables:
        if ds[var].dtype == 'float64':
            ds_out = ds_out.combine_first(
                dataarray_metrics(ds, var, 'Data_Referencia', diff=diff).astype(np.float32)
            )
        else:
            df_col = ds[var].to_dataframe().reset_index()[['CNPJ_Fundo', var]]
            df_col = df_col.groupby('CNPJ_Fundo').agg(
                lambda x: x.mode().iat[0]
            )
            
            if not isinstance(df_string, pd.DataFrame):
                df_string = df_col
            else:
                df_string[var] = df_col.values.astype(str)

    df_string['TIR'] = [ tir_fundo(ds, cnpj) for cnpj in ds.CNPJ_Fundo.values ]
    df_string['Data_Referencia_Inicial'] = ds['Patrimonio_Liquido'].to_dataframe().reset_index().dropna().drop(columns=['Patrimonio_Liquido']).groupby('CNPJ_Fundo').min()['Data_Referencia']
    df_string['Data_Referencia_Final'] = ds['Patrimonio_Liquido'].to_dataframe().reset_index().dropna().drop(columns=['Patrimonio_Liquido']).groupby('CNPJ_Fundo').max()['Data_Referencia']
    return ds_out, df_string
