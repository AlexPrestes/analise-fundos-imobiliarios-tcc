import os
import re
import urllib.request
import zipfile
from datetime import datetime
from functools import reduce

import pandas as pd


def download_files_cvm(report='mensal'):
    report = report.lower()
    year_now = int(datetime.now().strftime('%Y'))
    urls = [
        f'https://dados.cvm.gov.br/dados/FII/DOC/INF_{report.upper()}/DADOS/inf_{report.lower()}_fii_{ano}.zip'
        for ano in range(2016, year_now + 2)
    ]

    path_list = ['dataset', 'cvm', 'zip', f'{report}']
    path = ''

    for folder in path_list:
        path += f'{folder}/'
        if not os.path.exists(path):
            os.mkdir(path)

    for url in urls:
        filename = url.split('/')[-1]
        try:
            urllib.request.urlretrieve(url, f'{path}{filename}')
        except:
            ...

    return path, os.listdir(path)


def unzip_files_cvm(report='mensal'):
    report = report.lower()

    path_list = ['dataset', 'cvm', 'csv', f'{report}']
    path = ''

    for folder in path_list:
        path += f'{folder}/'
        if not os.path.exists(path):
            os.mkdir(path)

    path_zip = f'dataset/cvm/zip/{report}/'

    for filename in os.listdir(path_zip):
        with zipfile.ZipFile(f'{path_zip}{filename}', 'r') as zip_ref:
            zip_ref.extractall(path)

    return path, os.listdir(path)


def read_files_cvm(report='mensal'):
    report = report.lower()
    path = f'dataset/cvm/csv/{report}/'
    filenames = os.listdir(path)
    dict_df = {}

    for fn in filenames:
        df = pd.read_csv(path + fn, encoding='ISO-8859-1', sep=';')
        df_key = re.match(r'.*fii_(.*)_\d{4}\.csv', fn).group(1)
        dict_df[df_key] = pd.concat(
            [
                dict_df.get(df_key, pd.DataFrame()),
                df,
            ],
            ignore_index=True,
        )

    for df_key in dict_df.keys():
        dict_df[df_key].sort_values(
            list(dict_df[df_key]), inplace=True, ignore_index=True
        )

    return dict_df


def transform_files_cvm(report='mensal'):
    report = report.lower()
    if report != 'mensal':
        return

    dict_fundos = {}
    df = reduce(
        lambda df1, df2: pd.merge(df1, df2), read_files_cvm(report).values()
    )

    dict_fundos = {
        cnpj: df[df.CNPJ_Fundo == cnpj]
        .drop(columns=['CNPJ_Fundo'])
        .set_index(['Data_Referencia'])
        for cnpj in df.CNPJ_Fundo.unique()
    }

    return dict_fundos
