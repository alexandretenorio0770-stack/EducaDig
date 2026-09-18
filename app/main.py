import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

try:
    from wordcloud import WordCloud
    WORDCLOUD_DISPONIVEL = True
except ModuleNotFoundError:
    WORDCLOUD_DISPONIVEL = False

from src.api import buscar_municipios

# 2. Configuração da Página
st.set_page_config(page_title="EducaDig ESG", layout="wide")


@st.cache_data
def gerar_nuvem_palavras():
    with open("data/raw/texto_esg.txt", "r", encoding="utf-8") as f:
        texto = f.read()

    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(texto)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    return fig


# 3. Criação das Abas
aba_territorio, aba_noticias, aba_gestao = st.tabs([
    " Panorama Territorial",
    " Notícias & Nuvem de Palavras",
    " Gestão de Dados"
])

# --- ABA 1: PANORAMA TERRITORIAL ---
with aba_territorio:
    '''
    # EducaDig ESG

    #### Falta de visibilidade e centralização de dados públicos sobre a infraestrutura tecnológica de escolas públicas, o que dificulta o direcionamento eficiente de investimentos privados (ESG) e ações de ONGs para promover a inclusão digital em regiões vulneráveis.
    *ODS 4 - Educação de qualidade*

    **Links Úteis e Inspirações:**
    * [Agenda 2030 - ONU](https://brasil.un.org/pt-br/sdgs)
    * [Observatório do Terceiro Setor](https://observatorio3setor.org.br/)
    * [Conecta Brasil](https://conectabrasil.org/)
    '''

    st.sidebar.title("Sobre o Projeto")
    st.sidebar.info(
        "**Nota de Transparência:** Interface e código base desenvolvidos com o "
        "suporte de IA Generativa, em conformidade com o regimento do TP1 e TP2."
    )

    dados = buscar_municipios()
    df = pd.DataFrame(dados)
    st.dataframe(df, use_container_width=True)

# --- ABA 2: NOTÍCIAS & NUVEM DE PALAVRAS ---
with aba_noticias:
    '''
    # Notícias ESG
    '''
    st.info(
        "A aba de notícias apresenta as últimas matérias relacionadas a ESG e ODS 4, "
        "extraídas via Web Scraping. Além disso, é gerada uma nuvem de palavras com os termos mais frequentes."
    )

    st.subheader("Nuvem de Palavras das Notícias")
    
    # Chamada e renderização da função da Nuvem de Palavras
    if WORDCLOUD_DISPONIVEL:
        try:
            fig_nuvem = gerar_nuvem_palavras()
            st.pyplot(fig_nuvem)
        except FileNotFoundError:
            st.warning("Ficheiro 'data/raw/texto_esg.txt' não encontrado. Execute o script 'python src/scraping.py' primeiro.")
    else:
        st.warning("A biblioteca 'wordcloud' não está instalada no ambiente atual.")

    st.subheader("Conteúdos Extraídos sobre ODS 4 (BeautifulSoup)")
    try:
        df_noticias = pd.read_csv("data/raw/noticias_esg.csv")
        st.dataframe(df_noticias, use_container_width=True)
    except FileNotFoundError:
        st.warning("Execute o script 'python src/scraping.py' primeiro para gerar os dados.")

# --- ABA 3: GESTÃO DE DADOS ---
with aba_gestao:
    st.subheader("Serviço de Upload e Download de Ficheiros")
    st.write("Adicione novos ficheiros CSV ao sistema ou descarregue os relatórios.")

    if 'dados_usuario' not in st.session_state:
        st.session_state['dados_usuario'] = None

    ficheiro_carregado = st.file_uploader("Carregar ficheiro CSV", type=["csv"])

    if ficheiro_carregado is not None:
        df_uploaded = pd.read_csv(ficheiro_carregado)
        st.session_state['dados_usuario'] = df_uploaded
        st.success("Ficheiro carregado e guardado na sessão com sucesso!")

    if st.session_state['dados_usuario'] is not None:
        st.write("---")
        st.subheader("Dados Atuais na Sessão:")
        st.dataframe(st.session_state['dados_usuario'], use_container_width=True)

        csv_data = st.session_state['dados_usuario'].to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Descarregar Tabela em CSV",
            data=csv_data,
            file_name="dados_educadig_exportados.csv",
            mime="text/csv"
        )
    else:
        st.info("Nenhum ficheiro foi carregado ainda.")