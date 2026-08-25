import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
from src.api import buscar_municipios
'''
# EducaDig ESG

#### Falta de visibilidade e centralização de dados públicos sobre a infraestrutura tecnológica de escolas públicas, 
#### o que dificulta o direcionamento eficiente de investimentos privados (ESG) e ações de ONGs para promover a inclusão digital em regiões vulneráveis.
*ODS 4 - Educação de qualidade*

Links Úteis e Inspirações
* [Agenda 2030 - ONU](https://brasil.un.org/pt-br/sdgs)
* [Observatório do Terceiro Setor](https://observatorio3setor.org.br/)
* [Conecta Brasil](https://conectabrasil.org/)
'''

st.sidebar.title("Sobre o Projeto")
st.sidebar.info(
    "**Nota de Transparência:** Interface e código base desenvolvidos com o "
    "suporte de IA Generativa, em conformidade com o regimento do TP1."
)

dados = buscar_municipios()
df = pd.DataFrame(dados)
st.dataframe(df)