import streamlit as st
import pandas as pd
import requests
from pathlib import Path

# Caminho absoluto até a raiz EducaDig/ (recua de app/pages/assistente_ia.py)
RAIZ_PROJETO = Path(__file__).resolve().parent.parent.parent
CAMINHO_CSV = RAIZ_PROJETO / "data" / "raw" / "noticias_esg.csv"
API_URL = "http://127.0.0.1:8000"

st.header(" Inteligência Artificial Local & Consultor ESG (ODS 4)")
st.markdown(
    "Módulo integrado ao backend **FastAPI + Hugging Face** (`pysentimiento/bertweet-pt-sentiment`) "
    "para classificação editorial e análise conversacional com memória."
)

# Carregamento seguro do CSV para alimentar as opções de análise
df_noticias = pd.DataFrame()
if CAMINHO_CSV.exists():
    df_noticias = pd.read_csv(CAMINHO_CSV).fillna("")

aba_classificador, aba_chat = st.tabs([
    " Classificador de Sentimento (TP4)",
    " Assistente Conversacional ESG (TP5)"
])

# ==============================================================================
# ABA 1: CLASSIFICAÇÃO DE SENTIMENTO LOCAL (TP4)
# ==============================================================================
with aba_classificador:
    st.subheader("Análise de Polaridade Editorial")

    opcao_entrada = st.radio(
        "Selecione a origem do texto:",
        ["Escolher notícia extraída (CSV)", "Digitar texto manualmente"],
        horizontal=True
    )

    texto_analise = ""
    if opcao_entrada == "Escolher notícia extraída (CSV)" and not df_noticias.empty:
        coluna_texto = df_noticias.columns[0]
        texto_analise = st.selectbox(
            "Notícias coletadas:", df_noticias[coluna_texto].tolist())
    else:
        texto_analise = st.text_area(
            "Texto sobre Educação / ESG:",
            "Novas escolas públicas recebem laboratórios de informática e internet de alta velocidade."
        )

    if st.button("Classificar com IA Local", type="primary"):
        if len(texto_analise.strip()) < 10:
            st.warning("Insira um texto com pelo menos 10 caracteres.")
        else:
            with st.spinner("Processando no modelo local..."):
                try:
                    resp = requests.post(
                        f"{API_URL}/processar_texto",
                        json={"texto": texto_analise},
                        timeout=15
                    )
                    if resp.status_code == 200:
                        dados = resp.json()
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Polaridade", dados["sigla_classificacao"])
                        c2.metric(
                            "Confiança", f"{dados['confianca'] * 100:.2f}%")
                        c3.info(dados["interpretacao"])
                    else:
                        st.error(
                            f"Erro na API ({resp.status_code}): {resp.json().get('detail')}")
                except requests.exceptions.ConnectionError:
                    st.error(
                        "API FastAPI offline. Inicie o Uvicorn no outro terminal.")

# ==============================================================================
# ABA 2: ASSISTENTE COM MEMÓRIA CONVERSACIONAL (TP5)
# ==============================================================================
with aba_chat:
    st.subheader("Consultor Contextual com Memória")
    st.caption(
        "O sistema mantém o histórico da sessão para responder com base nas notícias coletadas.")

    if "historico_chat" not in st.session_state:
        st.session_state.historico_chat = [
            {
                "role": "assistant",
                "content": "Olá! Sou o consultor IA do EducaDig. Pergunte-me sobre os temas, avanços ou desafios encontrados nas notícias coletadas sobre Educação (ODS 4)."
            }
        ]

    if st.button("Limpar Memória da Conversa"):
        st.session_state.historico_chat = st.session_state.historico_chat[:1]
        st.rerun()

    col_limpar, col_exportar = st.columns(2)
    with col_limpar:
        if st.button(" Limpar Memória da Conversa", use_container_width=True):
            st.session_state.historico_chat = st.session_state.historico_chat[:1]
            st.rerun()

    with col_exportar:
        relatorio_txt = "\n\n".join(
            [f"[{m['role'].upper()}]: {m['content']}" for m in st.session_state.historico_chat]
        )
        st.download_button(
            label=" Exportar Sessão ESG (.txt)",
            data=relatorio_txt.encode("utf-8"),
            file_name="relatorio_consultor_educadig.txt",
            mime="text/plain",
            use_container_width=True
        )

    for msg in st.session_state.historico_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if pergunta := st.chat_input("Ex: Quais notícias abordam educação pública ou inclusão digital?"):
        st.session_state.historico_chat.append(
            {"role": "user", "content": pergunta})
        with st.chat_message("user"):
            st.markdown(pergunta)

        with st.chat_message("assistant"):
            with st.spinner("Analisando base de dados e contexto..."):
                try:
                    resp = requests.post(
                        f"{API_URL}/chat_esg",
                        json={
                            "pergunta": pergunta,
                            "historico": st.session_state.historico_chat[:-1]
                        },
                        timeout=15
                    )
                    if resp.status_code == 200:
                        resposta_ia = resp.json()["resposta"]
                        st.markdown(resposta_ia)
                        st.session_state.historico_chat.append(
                            {"role": "assistant", "content": resposta_ia})
                    else:
                        st.error(
                            f"Erro ({resp.status_code}): {resp.json().get('detail')}")
                except requests.exceptions.ConnectionError:
                    st.error(
                        "API FastAPI offline. Inicie o Uvicorn no outro terminal.")
