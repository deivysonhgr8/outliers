import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plotar_histograma_totais_por_regiao_original(dataframe: pd.DataFrame):
    """
    Análise 1: Histograma comparativo da distribuição do PIB TOTAL das UFs, agrupado por REGIÃO.
    """
    print("\n" + "="*50)
    print("Análise 1: Histograma dos PIBs Totais por Região (Original)")
    print("="*50)
    print("Gerando histograma da distribuição dos PIBs totais, separado por região...")

    # 1. Prepara os dados: Cria um DataFrame com o PIB total de cada UF e a sua respetiva região
    df_totais = dataframe.groupby(['nome_regiao', 'nome_uf'])['pib'].sum().reset_index()

    # 2. Cria o histograma com uma curva de densidade (kde) para cada região
    plt.figure(figsize=(12, 7))
    ax = sns.histplot(data=df_totais, x='pib', hue='nome_regiao', kde=True, palette='viridis')
    
    ax.set_title('Distribuição do PIB Total das UFs por Região', fontsize=20, pad=20)
    ax.set_xlabel('Valor do PIB Total por UF', fontsize=14)
    ax.set_ylabel('Contagem de UFs', fontsize=14)
    ax.ticklabel_format(style='plain', axis='x')
    formatter = plt.FuncFormatter(lambda x, pos: f'{x/1e9:,.0f} B')  #type: ignore
    ax.xaxis.set_major_formatter(formatter)
    plt.tight_layout()
    plt.show()

def plotar_histograma_totais_por_regiao_log(dataframe: pd.DataFrame):
    """
    Análise 2: Histograma comparativo da distribuição do PIB TOTAL (log) das UFs, agrupado por REGIÃO.
    """
    print("\n" + "="*50)
    print("Análise 2: Histograma dos PIBs Totais por Região (Log)")
    print("="*50)
    print("Gerando histograma da distribuição dos PIBs totais (escala log), separado por região...")

    # 1. Prepara os dados: Cria um DataFrame com o PIB total de cada UF e a sua respetiva região
    df_totais = dataframe.groupby(['nome_regiao', 'nome_uf'])['pib'].sum().reset_index()
    
    # 2. Aplica a transformação de log a esses valores totais
    df_totais['pib_log'] = np.log(df_totais['pib'])

    # 3. Cria o histograma com uma curva de densidade (kde) para cada região
    plt.figure(figsize=(12, 7))
    ax = sns.histplot(data=df_totais, x='pib_log', hue='nome_regiao', kde=True, palette='viridis')
    
    ax.set_title('Distribuição do PIB Total das UFs por Região (Escala Log)', fontsize=20, pad=20)
    ax.set_xlabel('Log do Valor do PIB Total por UF', fontsize=14)
    ax.set_ylabel('Contagem de UFs', fontsize=14)
    plt.tight_layout()
    plt.show()

def plotar_pib_por_uf_boxplot_original(dataframe: pd.DataFrame):
    """
    Análise 3: Gera um boxplot mostrando a DISTRIBUIÇÃO do PIB municipal por UF (dados originais).
    """
    print("\n" + "="*50)
    print("Análise 3: Distribuição do PIB Municipal por UF (Original)")
    print("="*50)
    uf_order = dataframe.groupby('nome_uf')['pib'].median().sort_values(ascending=False).index
    plt.figure(figsize=(20, 10))
    ax = sns.boxplot(data=dataframe, x='nome_uf', y='pib', order=uf_order, palette='viridis')
    ax.set_title('Distribuição do PIB Entre os Municípios de Cada UF', fontsize=20, pad=20)
    ax.set_xlabel('Unidade da Federação (UF)', fontsize=14)
    ax.set_ylabel('PIB dos Municípios (em R$)', fontsize=14)
    plt.xticks(rotation=90)
    ax.ticklabel_format(style='plain', axis='y')
    plt.tight_layout()
    plt.show()

def plotar_pib_por_uf_boxplot_log(dataframe: pd.DataFrame):
    """
    Análise 4: Gera um boxplot mostrando a DISTRIBUIÇÃO do PIB municipal por UF (dados transformados).
    """
    print("\n" + "="*50)
    print("Análise 4: Distribuição do PIB Municipal por UF (Pós-Transformação Log)")
    print("="*50)
    print("Gerando boxplot da distribuição municipal com dados transformados...")
    
    uf_order = dataframe.groupby('nome_uf')['pib'].median().sort_values(ascending=False).index
    plt.figure(figsize=(20, 10))
    ax = sns.boxplot(data=dataframe, x='nome_uf', y='pib_log', order=uf_order, palette='plasma')
    ax.set_title('Distribuição do PIB Municipal por UF (Após Transformação Log)', fontsize=20, pad=20)
    ax.set_xlabel('Unidade da Federação (UF)', fontsize=14)
    ax.set_ylabel('Log do PIB dos Municípios', fontsize=14)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def executar_analise_completa(dataframe: pd.DataFrame):
    sns.set_theme(style="whitegrid")
    print("\n--- INICIANDO ANÁLISE DA DISTRIBUIÇÃO DO PIB TOTAL (AGREGADO) POR REGIÃO ---")
    plotar_histograma_totais_por_regiao_original(dataframe)
    plotar_histograma_totais_por_regiao_log(dataframe)
    

    print("\n--- INICIANDO ANÁLISE DA DISTRIBUIÇÃO MUNICIPAL ---")
    plotar_pib_por_uf_boxplot_original(dataframe)
    plotar_pib_por_uf_boxplot_log(dataframe)

def apresentar_analise_zscore(df_outliers):
    print("\n" + "="*80)
    print("Análise de Outliers pelo Método Z-Score (Limiar |Z| > 3)")
    print("="*80)

    if df_outliers.empty:
        print("Nenhum outlier encontrado com o critério de Z-Score > 3.")
        return

    # Seleciona e reordena as colunas para uma apresentação clara
    colunas_display = [
        'nome_mun', 'nome_uf', 'pib', 'pib_zscore', 'pib_per_capta', 'pib_per_capta_zscore'
    ]
    df_display = df_outliers[colunas_display].copy()
    
    # Arredonda os valores para melhor visualização
    df_display['pib_zscore'] = df_display['pib_zscore'].round(2)
    df_display['pib_per_capta_zscore'] = df_display['pib_per_capta_zscore'].round(2)

    print("Municípios identificados como outliers em 'pib' ou 'pib_per_capta':")
    # Ordena pelos maiores Z-Scores para destacar os mais extremos
    print(df_display.sort_values(by=['pib_zscore', 'pib_per_capta_zscore'], ascending=False).to_string())

def plotar_outliers_isolation_forest(df_completo, df_outliers):

    print("Análise de Outliers pelo Método Isolation Forest")
    if df_outliers.empty:
        print("Nenhum outlier encontrado pelo Isolation Forest.")
        return
        
    # Cria uma figura com dois subplots, um para cada variável
    fig, axes = plt.subplots(1, 2, figsize=(20, 9))
    fig.suptitle('Deteção de Outliers com Isolation Forest', fontsize=22)
    
    # Gráfico para a variável 'pib' 
    sns.boxplot(data=df_completo, y='pib', ax=axes[0], color='lightblue')
    sns.stripplot(data=df_outliers, y='pib', ax=axes[0], color='red', s=8, label='Outliers Identificados')
    axes[0].set_title('Distribuição do PIB Municipal', fontsize=16)
    axes[0].set_ylabel('PIB dos Municípios (em R$)', fontsize=12)
    axes[0].ticklabel_format(style='plain', axis='y')
    axes[0].legend()
    
    # Gráfico para a variável 'pib_per_capta' 
    sns.boxplot(data=df_completo, y='pib_per_capta', ax=axes[1], color='lightgreen')
    sns.stripplot(data=df_outliers, y='pib_per_capta', ax=axes[1], color='red', s=8, label='Outliers Identificados')
    axes[1].set_title('Distribuição do PIB per Capita Municipal', fontsize=16)
    axes[1].set_ylabel('PIB per Capita (em R$)', fontsize=12)
    axes[1].ticklabel_format(style='plain', axis='y')
    axes[1].legend()

    plt.tight_layout(rect=(0, 0.03, 1, 0.95))
    plt.show()