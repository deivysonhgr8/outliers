import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()
def extrair_pib_dados(caminho_do_arquivo):
    try:
  
        df = pd.read_excel(caminho_do_arquivo,
                           usecols=[0, 1, 2, 3, 4, 5, 6, 7, 38, 39])
                        
        df.rename(columns={
            df.columns[0]: 'ano',
            df.columns[1]: 'cod_regiao',
            df.columns[2]: 'nome_regiao',
            df.columns[3]: 'cod_uf',
            df.columns[4]: 'sigla_uf',
            df.columns[5]: 'nome_uf',
            df.columns[6]: 'cod_mun',
            df.columns[7]: 'nome_mun',
            df.columns[8]: 'pib',
            df.columns[9]: 'pib_per_capta',
        }, inplace=True)
        df['pib'] = df['pib'] * 1000
        return df

    except FileNotFoundError:
        print(f"Erro: O arquivo não foi encontrado no caminho especificado: {caminho_do_arquivo}")
        return None
    except ValueError as e:
        print(f"Erro de valor ao ler o arquivo: {e}")
        print("Verifique se as colunas estão corretas.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return None

#teste da função
if __name__ == '__main__':
    caminho_do_arquivo = os.getenv('ARCHIVE_PATH')
    df_extraido = None
    if caminho_do_arquivo:
        df_extraido = extrair_pib_dados(caminho_do_arquivo)
        if df_extraido is not None:
            print("DataFrame extraído com sucesso:")
            print(df_extraido.head())
    if df_extraido is not None:
        print("DataFrame extraído com sucesso:")
        print(df_extraido.info())
        print("\nPrimeiras 5 linhas:")
        print(df_extraido.head())