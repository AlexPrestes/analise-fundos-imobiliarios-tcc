import os
import urllib.request  # Download
import zipfile  # Descompactar
from os import remove  # para apagar os arquivos já utilizados

# Biblioteca usada para leitura e união dos arquivos baixados
import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None


class DatasetCVM:
    def __init__(self, inf='mensal', periodo=[2016, 2022]):
        self.inf = inf
        self.periodo = periodo

    def run(self):
        self.columns_series()
        self.data_series()

    def download_files(self, inf, periodo):
        for ano in range(*periodo):
            url = f'https://dados.cvm.gov.br/dados/FII/DOC/INF_{inf.upper()}/DADOS/inf_{inf.lower()}_fii_{ano}.zip'
            filename = f'inf_{inf.lower()}_fii_{ano}.zip'
            urllib.request.urlretrieve(url, filename)

    def unzip_files(self, inf, periodo):
        for ano in range(*periodo):
            filename = f'inf_{inf.lower()}_fii_{ano}.zip'

            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall()

            remove(filename)

    def merge_files(self, inf, periodo, arquivos):
        df_dataset = pd.DataFrame()
        df_inf = pd.DataFrame()

        for nome_arquivo in arquivos:
            df_dataset = pd.DataFrame()

            for ano in range(*periodo):
                filename = (
                    f'inf_{inf.lower()}_fii_{nome_arquivo.lower()}_{ano}.csv'
                )

                if df_dataset.empty:
                    df_dataset = pd.read_csv(
                        filename, sep=';', decimal='.', encoding='iso-8859-1'
                    )

                remove(filename)

            if df_inf.empty:
                df_inf = df_dataset
            else:
                df_inf = pd.merge(df_inf, df_dataset, how='outer')

        df_inf['Data_Referencia'] = pd.to_datetime(df_inf['Data_Referencia'])

        return df_inf

    def informes(
        self,
        inf='mensal',
        periodo=[2016, 2022],
        arquivos=['geral', 'complemento', 'ativo_passivo'],
    ):
        periodo[1] += 1

        self.download_files(inf, periodo)
        self.unzip_files(inf, periodo)
        df_inf = self.merge_files(inf, periodo, arquivos)

        return df_inf

    def columns_series(self, list_col=[]):
        if list_col:
            self.list_columns_series = list_col
        else:
            self.list_columns_series = [
                'Valor_Patrimonial_Cotas',
                'Percentual_Despesas_Taxa_Administracao',
                'Percentual_Despesas_Agente_Custodiante',
                'Percentual_Rentabilidade_Efetiva_Mes',
                'Percentual_Rentabilidade_Patrimonial_Mes',
                'Percentual_Dividend_Yield_Mes',
                'Percentual_Amortizacao_Cotas_Mes',
                'Valor_Ativo',
                'Patrimonio_Liquido',
                'Disponibilidades',
                'Titulos_Publicos',
                'Titulos_Privados',
                'Fundos_Renda_Fixa',
                'Total_Investido',
                'Direitos_Bens_Imoveis',
                'Terrenos',
                'Imoveis_Renda_Acabados',
                'Imoveis_Renda_Construcao',
                'Imoveis_Venda_Acabados',
                'Imoveis_Venda_Construcao',
                'Outros_Direitos_Reais',
                'Acoes',
                'Debentures',
                'Bonus_Subscricao',
                'Certificados_Deposito_Valores_Mobiliarios',
                'Cedulas_Debentures',
                'Fundo_Acoes',
                'FIP',
                'FII',
                'FDIC',
                'Outras_Cotas_FI',
                'Notas_Promissorias',
                'Acoes_Sociedades_Atividades_FII',
                'Cotas_Sociedades_Atividades_FII',
                'CEPAC',
                'CRI',
                'Letras_Hipotecarias',
                'LCI',
                'LIG',
                'Outros_Valores_Mobliarios',
                'Valores_Receber',
                'Contas_Receber_Aluguel',
                'Contas_Receber_Venda_Imoveis',
                'Outros_Valores_Receber',
                'Rendimentos_Distribuir',
                'Taxa_Administracao_Pagar',
                'Taxa_Performance_Pagar',
                'Obrigacoes_Aquisicao_Imoveis',
                'Adiantamento_Venda_Imoveis',
                'Adiantamento_Alugueis',
                'Obrigacoes_Securitizacao_Recebiveis',
                'Instrumentos_Financeiros_Derivativos',
                'Provisoes_Contigencias',
                'Outros_Valores_Pagar',
                'Total_Passivo',
            ]

    def data_series(self):
        data = self.informes(self.inf, self.periodo)
        self.data_info = self.data_info(data)
        self.data = (
            data[['CNPJ_Fundo', 'Data_Referencia'] + self.list_columns_series]
            .sort_values(['CNPJ_Fundo', 'Data_Referencia'])[
                ['CNPJ_Fundo'] + self.list_columns_series
            ]
            .fillna(0)
            .groupby('CNPJ_Fundo')
            .agg(list)
        )

    def data_info(self, data):
        data_info = data[
            [
                'CNPJ_Fundo',
                'Publico_Alvo',
                'Fundo_Exclusivo',
                'Cotistas_Vinculo_Familiar',
                'Mandato',
                'Segmento_Atuacao',
                'Tipo_Gestao',
                'Prazo_Duracao',
            ]
        ]

        data_info['Publico_Alvo'] = data_info['Publico_Alvo'].apply(
            lambda x: x if isinstance(x, str) else 'INVESTIDORES EM GERAL'
        )
        data_info['Publico_Alvo'] = data_info['Publico_Alvo'].apply(
            lambda x: x
            if isinstance(x, np.ndarray)
            else 'INVESTIDORES EM GERAL'
        )

        data_info['Fundo_Exclusivo'] = data_info['Fundo_Exclusivo'].apply(
            lambda x: x if isinstance(x, str) else 'N'
        )
        data_info['Fundo_Exclusivo'] = data_info['Fundo_Exclusivo'].apply(
            lambda x: x if isinstance(x, np.ndarray) else 'N'
        )

        data_info['Cotistas_Vinculo_Familiar'] = data_info[
            'Cotistas_Vinculo_Familiar'
        ].apply(lambda x: x if isinstance(x, str) else 'N')
        data_info['Cotistas_Vinculo_Familiar'] = data_info[
            'Cotistas_Vinculo_Familiar'
        ].apply(lambda x: x if isinstance(x, np.ndarray) else 'N')

        data_info['Mandato'] = data_info['Mandato'].apply(
            lambda x: x if isinstance(x, str) else 'Renda'
        )
        data_info['Mandato'] = data_info['Mandato'].apply(
            lambda x: x if isinstance(x, np.ndarray) else 'Renda'
        )

        data_info['Segmento_Atuacao'] = data_info['Segmento_Atuacao'].apply(
            lambda x: x if isinstance(x, str) else 'Híbrido'
        )
        data_info['Segmento_Atuacao'] = data_info['Segmento_Atuacao'].apply(
            lambda x: x if isinstance(x, np.ndarray) else 'Híbrido'
        )

        data_info['Tipo_Gestao'] = data_info['Tipo_Gestao'].apply(
            lambda x: x if isinstance(x, str) else 'Passiva'
        )
        data_info['Tipo_Gestao'] = data_info['Tipo_Gestao'].apply(
            lambda x: x if isinstance(x, np.ndarray) else 'Passiva'
        )

        data_info['Prazo_Duracao'] = data_info['Prazo_Duracao'].apply(
            lambda x: x if isinstance(x, str) else 'Indeterminado'
        )
        data_info['Prazo_Duracao'] = data_info['Prazo_Duracao'].apply(
            lambda x: x if isinstance(x, np.ndarray) else 'Indeterminado'
        )

        data_info = data_info.groupby(['CNPJ_Fundo']).agg(
            lambda x: pd.Series.mode(x)
        )
        data_info['Data_Referencia'] = (
            data[['CNPJ_Fundo', 'Data_Referencia']]
            .groupby(['CNPJ_Fundo'])
            .agg(lambda x: pd.Series.max(x))['Data_Referencia']
        )

        return data_info
