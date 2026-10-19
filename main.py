import streamlit as st

st.set_page_config(page_title="Home", layout="wide")

st.title('Seja bem-vindo ao EducaDig')

panorama_page = st.Page("app/pages/panorama.py", title="Panorama Teritorisal")
noticias_page = st.Page("app/pages/noticias_ods.py", title="Noticias e ODS4")
gestao_page = st.Page("app/pages/gestao.py", title="Gestão de dados")
consumo_page = st.Page("app/pages/consumoAPI.py", title="API")

pg = st.navigation({
    'Principal': [panorama_page, noticias_page, gestao_page],
    'API': [consumo_page]
})

# 3. Execute a navegação (obrigatório para renderizar a página selecionada)
pg.run()
