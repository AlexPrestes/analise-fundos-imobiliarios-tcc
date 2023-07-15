import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt


list_metricas = ['average_clustering', 'coefficient_distribution_degree', 'density', 'average_degree', 'average_short_path']
#list_metricas = ['coefficient_distribution_degree']

list_variables = [
    'Valor_Ativo',
    #'Patrimonio_Liquido',
    #'Cotas_Emitidas',
    #'Valor_Patrimonial_Cotas',
    'Percentual_Despesas_Taxa_Administracao',
    'Percentual_Despesas_Agente_Custodiante',
    #'Percentual_Rentabilidade_Efetiva_Mes',
    #'Percentual_Rentabilidade_Patrimonial_Mes',
    #'Percentual_Dividend_Yield_Mes',
    #'Percentual_Amortizacao_Cotas_Mes',
    'Total_Necessidades_Liquidez',
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
    #'Quantidade_Cotas_Emitidas',
 ]

list_cat = [
    'Mandato',
    'Segmento_Atuacao',
    #'Publico_Alvo',
    #'Tipo_Gestao',
]

ds_fii = xr.open_dataset('dataset/cvm/dataset_cvm_metrica_mensal.nc').fillna(0)
df_dados_fii = pd.read_csv('dataset/cvm/dataset_cvm_metrica_mensal_dados.csv', index_col='CNPJ_Fundo')

df_dados_fii['Periodo'] = (pd.to_datetime(df_dados_fii['Data_Referencia_Final']) - pd.to_datetime(df_dados_fii['Data_Referencia_Inicial'])) / np.timedelta64(1, 'M')

df_fii = ds_fii.sel(metrica=list_metricas).to_array().sel(CNPJ_Fundo=(ds_fii.Acoes.sel(metrica='number_of_nodes') >= 24).values).sel(variable=list_variables).stack(var=['variable', 'metrica']).to_pandas()
df_fii['TIR'] = df_dados_fii['TIR'].fillna(-1)
df_fii_cat =  df_dados_fii[list_cat]
df_fii = df_fii[(df_fii[('TIR','')] <= 1) & (df_fii[('TIR','')] >= -1)]

cnpj_meses = xr.open_dataset('dataset/cvm/dataset_cvm_metrica_mensal.nc').fillna(0).Acoes.sel(metrica='number_of_nodes').to_pandas()

def select_cols(numbers):
    grupos_fiis = df_dados_fii[list_cat].dropna().agg('-'.join, axis=1)

    set_cols = set()

    for grupo in np.unique(grupos_fiis.values):
        cnpj_grupo = grupos_fiis[grupos_fiis==grupo].index.values


        df_dados = df_fii[df_fii.index.isin(cnpj_grupo)]
        corr = df_dados.corr()
        cols = corr['TIR'][corr['TIR'].abs() >= 0.0].abs().sort_values(ascending=False).index.values[1:(numbers+1)]

        for t in cols:
            set_cols.add(t)

    return list(set_cols)

from sklearn.ensemble import RandomForestRegressor

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split

from sklearn.metrics import mean_absolute_error

from sklearn.preprocessing import OneHotEncoder

preprocessing = OneHotEncoder().fit_transform(df_fii_cat[df_fii_cat.index.isin(df_fii.index.values)]).toarray()

score = {}
score_cat = {}

for k in range(10):
    print(f'k: {k}')
    cols_corr = select_cols(k+1)

    features = df_fii[ cols_corr ].values
    features_cat = np.hstack((features, preprocessing))
    target = df_fii[('TIR','')]
    std_target = target.fillna(-1.).values.flatten()

    models = [ RandomForestRegressor(n_jobs=-1) ]
    clf = []

    for i, model in enumerate(models):
        clf.append(make_pipeline(StandardScaler(), model))
        score_train = []
        score_test = []
        score[clf[i].steps[1][0]] = score.get(clf[i].steps[1][0], {})

        for j in range(10):
            print(f'j-1: {j}')
            X_train, X_test, y_train, y_test = train_test_split(features, std_target, test_size=0.33)

            clf[i].fit(X_train, y_train)
            
            score_train_i = mean_absolute_error(y_train, clf[i].predict(X_train))
            score_test_i = mean_absolute_error(y_test, clf[i].predict(X_test))

            score_train.append(score_train_i)
            score_test.append(score_test_i)
        
        score[clf[i].steps[1][0]][features.shape[1]] = score[clf[i].steps[1][0]].get(features.shape[1], {'train': score_train, 'test': score_test})


        score_train = []
        score_test = []
        score_cat[clf[i].steps[1][0]] = score_cat.get(clf[i].steps[1][0], {})

        for j in range(10):
            print(f'j-2: {j}')
            X_train, X_test, y_train, y_test = train_test_split(features_cat, std_target, test_size=0.33)

            clf[i].fit(X_train, y_train)

            score_train_i = mean_absolute_error(y_train, clf[i].predict(X_train))
            score_test_i = mean_absolute_error(y_test, clf[i].predict(X_test))

            score_train.append(score_train_i)
            score_test.append(score_test_i)

        score_cat[clf[i].steps[1][0]][features_cat.shape[1]] = score_cat[clf[i].steps[1][0]].get(features_cat.shape[1], {'train': score_train, 'test': score_test})

n = len(score)

fig, ax = plt.subplots(n, 2, figsize=(15, n*5))

for i in range(n):
    m = list(score.keys())[i]
    x_features = []
    y_train_mean = []
    y_train_std = []
    y_test_mean = []
    y_test_std = []

    for k in score[m]:
        x_features.append(k)
        y_train_mean.append(np.mean(score[m][k]['train']))
        y_train_std.append(np.std(score[m][k]['train']))
        y_test_mean.append(np.mean(score[m][k]['test']))
        y_test_std.append(np.std(score[m][k]['test']))

    x_features = np.asarray(x_features)
    y_train_mean = np.asarray(y_train_mean)
    y_train_std = np.asarray(y_train_std)
    y_test_mean = np.asarray(y_test_mean)
    y_test_std = np.asarray(y_test_std)

    if n == 1:
        ax[0].plot(x_features, y_test_mean, label='Teste', color='tab:blue')
        ax[0].fill_between(x_features, y_test_mean-y_test_std, y_test_mean+y_test_std, alpha=0.2, color='tab:blue')

        ax[0].plot(x_features, y_train_mean, label='Treino', color='tab:orange')
        ax[0].fill_between(x_features, y_train_mean-y_train_std, y_train_mean+y_train_std, alpha=0.2, color='tab:orange')

        ax[0].set_xlabel('Quantidade de variáveis')
        ax[0].set_ylabel('MAPE')
        ax[0].set_yscale('log')
        ax[0].set_title(m)
        ax[0].legend(loc='best')
    
    else:
        ax[i][0].plot(x_features, y_test_mean, label='Teste', color='tab:blue')
        ax[i][0].fill_between(x_features, y_test_mean-y_test_std, y_test_mean+y_test_std, alpha=0.2, color='tab:blue')

        ax[i][0].plot(x_features, y_train_mean, label='Treino', color='tab:orange')
        ax[i][0].fill_between(x_features, y_train_mean-y_train_std, y_train_mean+y_train_std, alpha=0.2, color='tab:orange')

        ax[i][0].set_xlabel('Quantidade de variáveis')
        ax[i][0].set_ylabel('MAPE')
        ax[i][0].set_title(m)
        ax[i][0].legend(loc='best')


for i in range(n):
    m = list(score_cat.keys())[i]
    x_features = []
    y_train_mean = []
    y_train_std = []
    y_test_mean = []
    y_test_std = []

    for k in score_cat[m]:
        x_features.append(k)
        y_train_mean.append(np.mean(score_cat[m][k]['train']))
        y_train_std.append(np.std(score_cat[m][k]['train']))
        y_test_mean.append(np.mean(score_cat[m][k]['test']))
        y_test_std.append(np.std(score_cat[m][k]['test']))

    x_features = np.asarray(x_features)
    y_train_mean = np.asarray(y_train_mean)
    y_train_std = np.asarray(y_train_std)
    y_test_mean = np.asarray(y_test_mean)
    y_test_std = np.asarray(y_test_std)

    if n == 1:
        ax[1].plot(x_features, y_test_mean, label='Teste', color='tab:blue')
        ax[1].fill_between(x_features, y_test_mean-y_test_std, y_test_mean+y_test_std, alpha=0.2, color='tab:blue')

        ax[1].plot(x_features, y_train_mean, label='Treino', color='tab:orange')
        ax[1].fill_between(x_features, y_train_mean-y_train_std, y_train_mean+y_train_std, alpha=0.2, color='tab:orange')

        ax[1].set_xlabel('Quantidade de variáveis')
        ax[1].set_ylabel('MAE')
        ax[1].set_yscale('log')
        ax[1].set_title(f'{m} com Categorias')
        ax[1].legend(loc='best')

    else:
        ax[i][1].plot(x_features, y_test_mean, label='Teste', color='tab:blue')
        ax[i][1].fill_between(x_features, y_test_mean-y_test_std, y_test_mean+y_test_std, alpha=0.2, color='tab:blue')

        ax[i][1].plot(x_features, y_train_mean, label='Treino', color='tab:orange')
        ax[i][1].fill_between(x_features, y_train_mean-y_train_std, y_train_mean+y_train_std, alpha=0.2, color='tab:orange')

        ax[i][1].set_xlabel('Quantidade de variáveis')
        ax[i][1].set_ylabel('MAE')
        ax[i][1].set_title(f'{m} com Categorias')
        ax[i][1].legend(loc='best')


plt.tight_layout()
plt.show()
