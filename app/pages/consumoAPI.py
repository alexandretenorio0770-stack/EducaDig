import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Consumo da API FastAPI")
st.write("Esta página faz requisições em tempo real para o servidor FastAPI backend.")

aba_get, aba_post = st.tabs([ 
    "Rota GET (Buscar Dados)",
    "Rota POST (Enviar Dados)"
])

# ==============================================================================
# ABA 1: ROTA GET (/noticias)
# ==============================================================================
with aba_get:
    st.header("Últimas Notícias")
    st.write("Clique no botão para buscar a tabela de notícias da API.")

    if st.button("Buscar Notícias"):
        try:
            resposta = requests.get(f"{API_URL}/noticias", timeout=15)

            if resposta.status_code == 200:
                payload = resposta.json()
                noticias = payload.get("dados", [])
                fonte = payload.get("fonte", "noticias_esg.csv")

                st.success(f"{payload.get('total', len(noticias))} notícias carregadas da fonte `{fonte}`.")
                df_noticias = pd.DataFrame(noticias)
                st.dataframe(df_noticias, use_container_width=True)
            else:
                detalhe = resposta.json().get("detail", f"Código de status: {resposta.status_code}")
                st.error(f"Erro na API ({resposta.status_code}): {detalhe}")

        except requests.exceptions.ConnectionError:
            st.error("API FastAPI offline. Certifique-se de que o Uvicorn está rodando na porta 8000.")
        except Exception as e:
            st.error(f"Erro inesperado ao consultar a API: {e}")

# ==============================================================================
# ABA 2: ROTA POST (/processar_texto)
# ==============================================================================
with aba_post:
    st.header("Analisar Texto / Manchete ESG")
    st.write("Envie um texto para o endpoint `POST /processar_texto` da API classificar o sentimento.")

    texto_usuario = st.text_area(
        "Digite ou cole o texto da notícia (mínimo de 10 caracteres):",
        placeholder="Ex: Projeto leva internet de alta velocidade e laboratórios digitais para escolas públicas."
    )

    if st.button("Enviar para Análise", type="primary"):
        try:
            resposta = requests.post(
                f"{API_URL}/processar_texto",
                json={"texto": texto_usuario},
                timeout=30
            )

            if resposta.status_code == 200:
                dados = resposta.json()
                st.success("Texto processado com sucesso pela API!")

                col1, col2, col3 = st.columns(3)
                col1.metric("Classificação", dados["sigla_classificacao"])
                col2.metric("Confiança", f"{dados['confianca'] * 100:.1f}%")
                col3.metric("Modelo", dados["modelo_utilizado"].split("/")[-1])

                st.info(f"**Interpretação ODS 4:** {dados['interpretacao']}")
                with st.expander("Ver JSON bruto retornado pela API"):
                    st.json(dados)
            else:
                detalhe = resposta.json().get("detail", f"Código de status: {resposta.status_code}")
                st.error(f"Erro na API ({resposta.status_code}): {detalhe}")

        except requests.exceptions.ConnectionError:
            st.error("API FastAPI offline. Certifique-se de que o Uvicorn está rodando na porta 8000.")
        except Exception as e:
            st.error(f"Erro inesperado ao enviar dados para a API: {e}")