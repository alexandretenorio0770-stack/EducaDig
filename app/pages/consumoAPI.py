import streamlit as st
import requests
import pandas as pd

api_url = ('http://127.0.0.1:8000')

st.title('Consumo da API FastAPI')
st.write('Esta página faz requisições em tempo real para o servidor FastAPI backend.')

# Criando duas abas para separar os testes de GET e POST
aba_get, aba_post = st.tabs([' Rota GET (Buscar Dados)', ' Rota POST (Enviar Dados)'])

# ---------------------------------------------------------
# 1. TESTANDO REQUISIÇÃO GET
# ---------------------------------------------------------
with aba_get:
    
    st.header("Últimas Notícias")
    st.write("Clique no botão para buscar a tabela de notícias da API.")
    
    if st.button("Buscar Notícias"):
        try:
            # Faz a requisição na rota exata definida no seu backend
            resposta = requests.get(f"{api_url}/api/v1/noticias")
            
            if resposta.status_code == 200:
                st.success("Notícias carregadas!")
                
                # 1. Captura o dicionário completo do JSON
                json_completo = resposta.json()
                
                # 2. Acessa a chave 'df' que contém a lista de registros
                lista_noticias = json_completo['df']
                
                # 3. Transforma a lista de volta em um DataFrame do Pandas
                df_recebido = pd.DataFrame(lista_noticias)
                
                # 4. Exibe na tela do Streamlit
                st.dataframe(df_recebido, use_container_width=True)
                
            else:
                st.error(f"Erro na API. Código de status: {resposta.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("Não foi possível conectar ao backend. Verifique se o Honcho está rodando.")

# ---------------------------------------------------------
# 2. TESTANDO REQUISIÇÃO POST
# ---------------------------------------------------------
with aba_post:
    st.header('Enviar Dados para o Servidor')
    st.write('Preencha o formulário para enviar dados via JSON (Exemplo: Cadastro).')
    
    # Criando campos de entrada baseados no que sua API espera receber
    # Ajuste os nomes dos campos conforme os atributos do seu modelo Pydantic do FastAPI
    titulo = st.text_input('Titulo da notícia:')
    link = st.text_input('link:')
    
    if st.button('Enviar Dados (POST)'):
        if titulo and link:
            # Monta o dicionário que será convertido em JSON automaticamente pelo requests
            payload = {
                'titulo': titulo,
                'link': link
            }
            
            try:
                # Faz a requisição enviando o payload no corpo da mensagem (json=payload)
                # Altere '/usuarios' para a rota de cadastro correta da sua API
                resposta = requests.post(f'{api_url}/usuarios', json=payload)
                
                if resposta.status_code in [200, 201]:
                    st.success('Dados enviados com sucesso!')
                    st.json(resposta.json())
                else:
                    st.error(f'Falha ao enviar. Status: {resposta.status_code}')
                    st.warning(resposta.text)
                    
            except requests.exceptions.ConnectionError:
                st.error('Erro de conexão. O servidor FastAPI está ativo?')
        else:
            st.warning('Por favor, preencha todos os campos antes de enviar.')