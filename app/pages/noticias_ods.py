import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

try:
    from wordcloud import WordCloud, STOPWORDS
    WORDCLOUD_DISPONIVEL = True
except ModuleNotFoundError:
    WORDCLOUD_DISPONIVEL = False

st.set_page_config(page_title="Noticias e ODS4", layout="wide")


@st.cache_data
def gerar_nuvem_palavras():
    with open("data/raw/texto_esg.txt", "r", encoding="utf-8") as f:
        texto = f.read()

    stopwords_pt = set(STOPWORDS)
    
    palavras_extras = {
        "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas", 
        "por", "para", "com", "um", "uma", "uns", "umas", "e", "o", "a", 
        "os", "as", "que", "se", "não", "mais", "como", "mas", "foi", 
        "ao", "ele", "ela", "ou", "seu", "sua", "quando", "muito", "já", 
        "está", "eu", "também", "só", "pelo", "pela", "até", "isso", 
        "entre", "depois", "sem", "mesmo", "aos", "suas", "quem", "num", "numa"
    }
    stopwords_pt.update(palavras_extras)

    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color="white",
        stopwords=stopwords_pt,
        max_words=100,
        colormap="viridis"
    ).generate(texto)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    
    return fig

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
    st.dataframe(df_noticias, width='stretch')
except FileNotFoundError:
    st.warning("Execute o script 'python src/scraping.py' primeiro para gerar os dados.")