from .extract import extrair_pib_dados
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def tratar_outliers_log(df_column):

    # Adiciona um valor pequeno para evitar log(0) ou log de negativo
    df_column_safe = df_column.copy()
    df_column_safe[df_column_safe <= 0] = 1e-6
    
    df_transformed = np.log(df_column_safe)
    
    # Retorna a coluna transformada e uma contagem simbólica de outliers (não usada)
    return df_transformed, 0

def identificar_outliers_zscore(df, colunas, threshold=3):

    df_com_zscore = df.copy()
    outliers_indices = []

    for col in colunas:
        if pd.api.types.is_numeric_dtype(df_com_zscore[col]):
            media = df_com_zscore[col].mean()
            desvio_padrao = df_com_zscore[col].std()
            
            if desvio_padrao > 0:
                z_score_col = f'{col}_zscore'
                df_com_zscore[z_score_col] = (df_com_zscore[col] - media) / desvio_padrao
                
                outliers_da_coluna = df_com_zscore[np.abs(df_com_zscore[z_score_col]) > threshold]
                outliers_indices.extend(outliers_da_coluna.index)

    if not outliers_indices:
        return pd.DataFrame()

    df_outliers = df.loc[list(set(outliers_indices))].copy()
    
    for col in colunas:
        z_score_col = f'{col}_zscore'
        if z_score_col in df_com_zscore.columns:
            df_outliers[z_score_col] = df_com_zscore.loc[df_outliers.index, z_score_col]
            
    return df_outliers

def identificar_outliers_iforest(df, colunas, random_state=42):

    X = df[colunas]
    iforest = IsolationForest(contamination='auto', random_state=random_state)
    previsoes = iforest.fit_predict(X)
    df_outliers = df[previsoes == -1].copy()
    return df_outliers

def obter_dados_processados(caminho_do_arquivo):

    df_extraido = extrair_pib_dados(caminho_do_arquivo)
    
    if df_extraido is None:
        # Garante que sempre retorna três valores, mesmo em caso de erro na extração
        return None, None, None
        
    # Tratamento de pib_per_capta negativo na Bahia
    linhas_negativas = (df_extraido['nome_uf'] == 'Bahia') & (df_extraido['pib_per_capta'] < 0)
    if linhas_negativas.any():
        print("Aviso: Valor(es) negativo(s) de 'pib_per_capta' encontrado(s) na Bahia.")
        print("Estes valores serão corrigidos para 0 antes da análise.")
        df_extraido.loc[linhas_negativas, 'pib_per_capta'] = 0
        
    # Agregação dos dados
    df_agregado = df_extraido.groupby(['nome_regiao','cod_mun', 'nome_mun', 'nome_uf']).agg(
        pib=('pib', 'mean'),
        pib_per_capta=('pib_per_capta', 'mean')
    ).reset_index()
    
    # Transformação Logarítmica
    colunas_a_tratar = ['pib', 'pib_per_capta']
    for col in colunas_a_tratar:
        df_agregado[f'{col}_log'], _ = tratar_outliers_log(df_agregado[col])
        
    # Análise de Outliers com Z-Score
    df_outliers_zscore = identificar_outliers_zscore(df_agregado, ['pib', 'pib_per_capta'])
    
    # Análise de Outliers com Isolation Forest
    df_outliers_iforest = identificar_outliers_iforest(df_agregado, ['pib', 'pib_per_capta'])
        
    return df_agregado, df_outliers_zscore, df_outliers_iforest