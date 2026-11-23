import streamlit as st
import pandas as pd
import requests
import subprocess
import sys
import matplotlib.pyplot as plt
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parent.parent.parent
CAMINHO_RAW = RAIZ_PROJETO / "data" / "raw" / "noticias_esg.csv"
CAMINHO_PROCESSED = RAIZ_PROJETO / "data" / "processed" / "noticias_classificadas.csv"
SCRIPT_SCRAPING = RAIZ_PROJETO / "src" / "scraping_dynamic.py"
API_URL = "http://127.0.0.1:8000"

st.header(" Orquestração do Pipeline de Dados & IA")
st.markdown("Execute o ciclo completo de Engenharia de Dados (Extração $\\rightarrow$ Enriquecimento LLM $\\rightarrow$ Exportação) diretamente pela interface.")

col_btn1, col_btn2 = st.columns(2)

# 1. Botão para executar o Selenium
with col_btn1:
    if st.button(" 1. Coletar Novas Notícias (Selenium)", use_container_width=True):
        with st.spinner("Executando WebDriver do Selenium no Observatório do 3º Setor..."):
            resultado = subprocess.run(
                [sys.executable, str(SCRIPT_SCRAPING)],
                capture_output=True,
                text=True
            )
            if resultado.returncode == 0:
                st.success("Coleta finalizada com sucesso!")
                st.code(resultado.stdout)
                st.rerun()
            else:
                st.error("Erro ao executar o scraping:")
                st.code(resultado.stderr)

# 2. Botão para classificar toda a base em lote via FastAPI
with col_btn2:
    if st.button(" 2. Classificar Toda a Base com IA (Lote)", type="primary", use_container_width=True):
        with st.spinner("Processando todas as notícias no modelo Hugging Face local..."):
            try:
                resp = requests.post(f"{API_URL}/processar_lote", timeout=60)
                if resp.status_code == 200:
                    dados = resp.json()
                    st.success(f"{dados['mensagem']} ({dados['total_processado']} registros)")
                    st.rerun()
                else:
                    st.error(f"Erro ({resp.status_code}): {resp.json().get('detail')}")
            except requests.exceptions.ConnectionError:
                st.error("API FastAPI offline. Certifique-se de que o Uvicorn está rodando.")

st.divider()

# 3. Visualização dos Dados Enriquecidos e Gráfico Macro
if CAMINHO_PROCESSED.exists():
    df_proc = pd.read_csv(CAMINHO_PROCESSED).fillna("")
    st.subheader(" Panorama de Sentimentos da Base Enriquecida")

    col_graf, col_tab = st.columns([1, 2])

    with col_graf:
        contagem = df_proc["sentimento"].value_counts()
        cores = {"POS": "#2ecc71", "NEU": "#3498db", "NEG": "#e74c3c"}
        lista_cores = [cores.get(idx, "#95a5a6") for idx in contagem.index]

        fig, ax = plt.subplots(figsize=(5, 4))
        contagem.plot(kind="bar", color=lista_cores, ax=ax)
        ax.set_title("Distribuição Editorial (ODS 4)")
        ax.set_xlabel("Polaridade")
        ax.set_ylabel("Qtd. de Notícias")
        plt.xticks(rotation=0)
        st.pyplot(fig)

    with col_tab:
        st.dataframe(df_proc, use_container_width=True)
        csv_bytes = df_proc.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=" Baixar Base Enriquecida (CSV)",
            data=csv_bytes,
            file_name="educadig_noticias_classificadas.csv",
            mime="text/csv"
        )
elif CAMINHO_RAW.exists():
    st.info("Base bruta encontrada. Clique no botão **2. Classificar Toda a Base com IA (Lote)** acima para gerar as colunas de sentimento e o gráfico.")
    st.dataframe(pd.read_csv(CAMINHO_RAW), use_container_width=True)
else:
    st.warning("Nenhuma base encontrada. Clique no botão **1. Coletar Novas Notícias** acima.")