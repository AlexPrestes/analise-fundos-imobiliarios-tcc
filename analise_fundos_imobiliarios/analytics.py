import warnings

from analise_fundos_imobiliarios.dataset import *
from analise_fundos_imobiliarios.dataset_cvm import *
from analise_fundos_imobiliarios.metrics import *

warnings.filterwarnings('ignore')


def dataarray_metrics(
    ds, variable='series', input_core_dims='time', metrics=None
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

    da_vg = xr.apply_ufunc(
        time_series_to_visibility_graph,
        ds[variable],
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


def metrics_fii_mensal(ds):
    variables = ds.to_array().coords['variable'].values[18:75]
    ds_out = dataarray_metrics(ds, variables[0], 'Data_Referencia')

    for var in variables[1:]:
        ds_out = ds_out.combine_first(
            dataarray_metrics(ds, var, 'Data_Referencia')
        )

    return ds_out
