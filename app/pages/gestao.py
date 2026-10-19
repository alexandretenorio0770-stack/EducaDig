import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestão", layout="wide")

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
    st.dataframe(st.session_state['dados_usuario'], width='stretch')

    csv_data = st.session_state['dados_usuario'].to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Descarregar Tabela em CSV",
        data=csv_data,
        file_name="dados_educadig_exportados.csv",
        mime="text/csv"
    )
else:
    st.info("Nenhum ficheiro foi carregado ainda.")