# Análise e Normalização do PIB Municipal (2010-2021)

## Objetivo do Projeto

Este projeto tem como objetivo principal a análise e o tratamento de dados de **Produto Interno Bruto (PIB) per capita e total dos municípios brasileiros** no período de 2010 a 2021. Utiliza a regra do Boxplot (IQR) para identificar **outliers** — valores extremos que podem distorcer a análise estatística —  e aplica a **transformação logarítmica** para normalizá-los.

O processo realizado segue a metodologia de **ETL (Extract, Transform, Load)**:
* **Extract**: Extração dos dados brutos de uma planilha excel.
* **Transform**: Limpeza dos nomes das colunas, identificação e tratamento dos outliers usando a função `log`.
* **Load**: Carregamento dos dados tratados em gráficos que explicam as conclusões obtidas.

## Instituições Envolvidas

Os dados utilizados neste projeto são de domínio público e foram fornecidos pelo **Instituto Brasileiro de Geografia e Estatística (IBGE)**, uma das principais fontes de estatísticas e informações geocientíficas do Brasil.

## Bibliotecas Utilizadas
Para rodar o script localmente, é necessário ter o Python e as bibliotecas listadas instaladas. Você pode instalar as dependências usando o `pip`, o gerenciador de pacotes do Python.

```bash
# Instale as bibliotecas necessárias
pip install -r requirements.txt

## Equipe de desenvolvimento:
- Deivyson Ribeiro
- Gustavo Henrique