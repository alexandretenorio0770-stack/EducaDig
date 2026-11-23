import streamlit as st

st.set_page_config(page_title="Home", layout="wide")

st.title('Seja bem-vindo ao EducaDig')

panorama_page = st.Page("app/pages/panorama.py", title="Panorama Territorial")
noticias_page = st.Page("app/pages/noticias_ods.py", title="Noticias e ODS4")
gestao_page = st.Page("app/pages/gestao.py", title="Gestão de dados")
consumo_page = st.Page("app/pages/consumoAPI.py", title="API")
ia_page = st.Page("app/pages/assistente_ia.py", title="Assistente IA (LLM)")

pg = st.navigation({
    'Principal': [panorama_page, noticias_page, gestao_page],
    'API & IA': [consumo_page, ia_page]
})

# 3. Execute a navegação (obrigatório para renderizar a página selecionada)
pg.run()
