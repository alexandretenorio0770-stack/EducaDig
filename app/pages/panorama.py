import streamlit as st
import pandas as pd
from src.api import buscar_municipios

st.set_page_config(page_title="Panorama Territorrial", layout="wide")

'''
# EducaDig ESG

#### Falta de visibilidade e centralização de dados públicos sobre a infraestrutura tecnológica de escolas públicas, o que dificulta o direcionamento eficiente de investimentos privados (ESG) e ações de ONGs para promover a inclusão digital em regiões vulneráveis.
*ODS 4 - Educação de qualidade*

**Links Úteis e Inspirações:**
* [Agenda 2030 - ONU](https://brasil.un.org/pt-br/sdgs)
* [Observatório do Terceiro Setor](https://observatorio3setor.org.br/)
* [Conecta Brasil](https://conectabrasil.org/)
'''

dados = buscar_municipios()
df = pd.DataFrame(dados)
st.dataframe(df, width='stretch')