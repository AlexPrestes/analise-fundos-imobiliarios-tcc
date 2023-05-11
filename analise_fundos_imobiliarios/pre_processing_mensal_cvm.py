import pandas as pd

pre_processing_mensal = {
    'CNPJ_Fundo': [r'(\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2})', str],
    #'Data_Referencia': [r'(\d{4}\-\d{2}\-\d{2})', pd.Timestamp],
    #'Data_Informacao_Numero_Cotistas': [r'(\d{4}\-\d{2}\-\d{2})', pd.Timestamp],
    #'Data_Entrega': [r'(\d{4}\-\d{2}\-\d{2})', pd.Timestamp],
    #'Data_Funcionamento': [r'(\d{4}\-\d{2}\-\d{2})', pd.Timestamp],
    'Publico_Alvo': [r'(INVESTIDORES\ EM\ GERAL|INVESTIDOR\ PROFISSIONAL|INVESTIDOR\ QUALIFICADO\ E\ PROFISSIONAL|INVESTIDOR\ QUALIFICADO)', str],
    'Codigo_ISIN': [r'(BR[\w\d]{4}[\w\d]{3}[\w\d]{2}\d)', str],
    'Fundo_Exclusivo': [r'(S|N)', str],
    'Cotistas_Vinculo_Familiar': [r'(S|N)', str],
    'Mandato': [r'(Renda|Desenvolvimento\ para\ Venda|Desenvolvimento\ para\ Renda|Híbrido|Títulos\ e\ Valores\ Mobiliários)', str],
    'Segmento_Atuacao': [r'(Shoppings|Híbrido|Lajes\ Corporativas|Outros|Logística|Hospital|Títulos\ e\ Val\.\ Mob\.|Hotel|Residencial)', str],
    'Tipo_Gestao': [r'(Passiva|Ativa)', str],
    'Prazo_Duracao': [r'(Indeterminado|Determinado)', str],
    #'Data_Prazo_Duracao': [r'(\d{4}\-\d{2}\-\d{2})', pd.Timestamp],
    'Encerramento_Exercicio_Social': [r'(\d{2}\/\d{2})', str]
}
