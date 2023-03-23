import os
import re
import urllib.request  # Download
import zipfile  # Descompactar
from datetime import date, datetime

import numpy as np
import pandas as pd
import xarray as xr


class DatasetFiiMensal:
    def download_files(self, inf):
        list_files = []
        ano_atual = int(datetime.now().strftime('%Y'))

        for ano in range(2016, ano_atual + 2):
            url = f'https://dados.cvm.gov.br/dados/FII/DOC/INF_{inf.upper()}/DADOS/inf_{inf.lower()}_fii_{ano}.zip'
            filename = f'inf_{inf.lower()}_fii_{ano}.zip'
            try:
                urllib.request.urlretrieve(url, filename)
                list_files.append(filename)
            except:
                ...

        return list_files

    def unzip_files(self, files):
        list_files = []

        for filename in files:
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall()
                for fn in zip_ref.filelist:
                    list_files.append(fn.filename)

            os.remove(filename)
        return list_files

    def concat_files(self, files, type_file):
        df = []
        for fn in files:
            if type_file in fn:
                if isinstance(df, pd.DataFrame):
                    df = pd.concat(
                        [
                            df,
                            pd.read_csv(
                                fn, encoding='ISO-8859-1', sep=';', decimal='.'
                            ),
                        ]
                    )
                else:
                    df = pd.read_csv(
                        fn, encoding='ISO-8859-1', sep=';', decimal='.'
                    )
                os.remove(fn)

        return df

    def list_type_files(self, list_filename):
        list_tf = []

        for fn in list_filename:
            tf = re.search(r'.*_fii_(.+?)_\d{4}\.csv', fn).group(1)
            if tf not in list_tf:
                list_tf.append(tf)

        return list_tf

    def list_pk_dataframe(self, df1, df2):
        index_pk = np.isin(df1.columns.values, df2.columns.values)
        return list(df1.columns.values[index_pk])

    def merge_dataframe(self, lista_arquivos_csv):
        list_df = []

        for tf in self.list_type_files(lista_arquivos_csv):
            df = self.concat_files(lista_arquivos_csv, tf)
            list_df.append(df)

        df = list_df[0]

        for df_i in list_df[1:]:
            df = df.merge(
                df_i,
                left_on=self.list_pk_dataframe(df, df_i),
                right_on=self.list_pk_dataframe(df, df_i),
            )

        return df

    def dataframe_to_dataset_mensal(
        self, df, index_cols, cols_string, cols_date
    ):
        index_cnpj_fundo = df[index_cols[0]].astype(str).unique()
        index_data_referencia = pd.to_datetime(df[index_cols[1]].unique())
        cols_float = df.drop(
            index_cols + cols_string + cols_date, axis=1
        ).columns.values.astype(str)

        data_string = xr.DataArray(
            dims=['cnpj_fundo', 'data_referencia', 'campo'],
            coords=[index_cnpj_fundo, index_data_referencia, cols_string],
            attrs=dict(describe='Dados formato de texto'),
        ).astype(str)

        for cnpj in index_cnpj_fundo:
            data_string.loc[
                cnpj,
                df[df.CNPJ_Fundo == cnpj].Data_Referencia.values,
                cols_string,
            ] = df[df.CNPJ_Fundo == cnpj][cols_string].to_numpy()

        data_date = xr.DataArray(
            dims=['cnpj_fundo', 'data_referencia', 'campo'],
            coords=[index_cnpj_fundo, index_data_referencia, cols_date],
            attrs=dict(describe='Dados formato data'),
        ).astype(date)

        for cnpj in index_cnpj_fundo:
            data_date.loc[
                cnpj,
                df[df.CNPJ_Fundo == cnpj].Data_Referencia.values,
                cols_date,
            ] = df[df.CNPJ_Fundo == cnpj][cols_date].to_numpy()

        data_float = xr.DataArray(
            dims=['cnpj_fundo', 'data_referencia', 'campo'],
            coords=[index_cnpj_fundo, index_data_referencia, cols_float],
            attrs=dict(describe='Dados formato numérico'),
        ).astype(np.float32)

        for cnpj in index_cnpj_fundo:
            data_float.loc[
                cnpj,
                df[df.CNPJ_Fundo == cnpj].Data_Referencia.values,
                cols_float,
            ] = df[df.CNPJ_Fundo == cnpj][cols_float].to_numpy()

        data = xr.Dataset(
            data_vars=dict(
                text=data_string,
                time=data_date,
                numeric=data_float,
            ),
            attrs=dict(
                describe="Dataset Informes Mensais FII's",
            ),
        )

        return data

    def run(self):
        lista_arquivos_zip = self.download_files('mensal')
        lista_arquivos_csv = self.unzip_files(lista_arquivos_zip)
        df = self.merge_dataframe(lista_arquivos_csv)

        index_dims = ['CNPJ_Fundo', 'Data_Referencia']

        fields_date = [
            'Data_Entrega',
            'Data_Funcionamento',
            'Data_Prazo_Duracao',
            'Data_Informacao_Numero_Cotistas',
        ]

        fields_string = [
            'Nome_Fundo',
            'Publico_Alvo',
            'Codigo_ISIN',
            'Fundo_Exclusivo',
            'Cotistas_Vinculo_Familiar',
            'Mandato',
            'Segmento_Atuacao',
            'Tipo_Gestao',
            'Prazo_Duracao',
            'Encerramento_Exercicio_Social',
            'Mercado_Negociacao_Bolsa',
            'Mercado_Negociacao_MBO',
            'Mercado_Negociacao_MB',
            'Entidade_Administradora_BVMF',
            'Entidade_Administradora_CETIP',
            'Nome_Administrador',
            'CNPJ_Administrador',
            'Logradouro',
            'Numero',
            'Complemento',
            'Bairro',
            'Cidade',
            'Estado',
            'CEP',
            'Telefone1',
            'Telefone2',
            'Telefone3',
            'Site',
            'Email',
        ]

        self.data = self.dataframe_to_dataset_mensal(
            df, index_dims, fields_string, fields_date
        )
