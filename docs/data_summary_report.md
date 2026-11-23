# Data Summary Report — Projeto EducaDig ESG

## 1. Visão Geral das Fontes de Dados
O projeto **EducaDig ESG** utiliza dados reais coletados da web para monitorar o debate público e as iniciativas relacionadas à Educação de Qualidade e Inclusão Digital (**ODS 4 — Agenda 2030**).

* **Fonte Principal:** Portal *Observatório do Terceiro Setor* (`https://observatorio3setor.org.br/`).
* **Método de Coleta:** Web scraping dinâmico automatizado via `Selenium` (`src/scraping_dynamic.py`), capaz de aguardar a renderização de elementos assíncronos em JavaScript.
* **Armazenamento Persistente:** Os registros extraídos são estruturados com `pandas` e gravados em `data/raw/noticias_esg.csv` (codificação `UTF-8`), utilizando gerenciamento dinâmico de caminhos absolutos (`pathlib`) para garantir portabilidade entre ambientes.

## 2. Pré-processamento e Qualidade dos Dados
Para transformar os textos brutos coletados em insumos analíticos e alimentadores de modelos de IA, foram aplicadas as seguintes etapas:

* **Tratamento de Nulos e Padronização:** Remoção de espaços excedentes (`strip()`) e preenchimento preventivo de valores ausentes (`fillna("")`) na leitura da API e do dashboard.
* **Mineração de Texto (NLP):** Filtragem personalizada de *stopwords* da língua portuguesa (artigos, preposições e conectivos) para isolar os termos de maior relevância semântica na geração da Nuvem de Palavras (`WordCloud`).
* **Preparação para Inferência LLM:** Truncamento controlado de tokens (`max_length=512`) na camada da API para adequação à janela de contexto da arquitetura BERTweet sem comprometer a memória RAM local.

## 3. Fluxo de Integração (Pipeline Completo)
1. **Extração (`scraping_dynamic.py`):** Coleta as manchetes e conteúdos dinâmicos e salva em `data/raw/noticias_esg.csv`.
2. **Serviço Backend (`src/api_fastapi.py`):** Expõe os dados via REST (`GET /noticias`), realiza classificação de polaridade (`POST /processar_texto`) e gerencia consultas contextuais (`POST /chat_esg`).
3. **Orquestração (`Procfile`):** Inicializa simultaneamente o servidor Uvicorn (porta `8000`) e a interface Streamlit (porta `8501`).
4. **Camada Visual (`main.py` e `app/pages/`):** Apresenta o panorama territorial, indicadores do ODS 4, nuvem de palavras, classificador de sentimentos e assistente conversacional em tempo real.