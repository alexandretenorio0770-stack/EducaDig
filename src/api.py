import requests
import pandas as pd

url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/35/municipios'


def buscar_municipios():
    resposta = requests.get(url)
    if resposta.status_code == 200:
        dados = resposta.json()
        
        # 1. Achata o JSON aninhado em um DataFrame
        df = pd.json_normalize(dados)
        
        # 2. Seleciona apenas as colunas desejadas usando a notação de ponto
        colunas_desejadas = [
            "id", 
            "nome", 
            "microrregiao.nome", 
            "microrregiao.mesorregiao.nome"
        ]
        df_filtrado = df[colunas_desejadas].copy()
        
        # 3. Renomeia as colunas para nomes mais amigáveis
        df_filtrado.columns = [
            "ID Município", 
            "Município", 
            "Microrregião", 
            "Mesorregião"
        ]
        
        return df_filtrado
