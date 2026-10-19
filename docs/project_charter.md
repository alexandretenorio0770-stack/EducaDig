# 📋 Project Charter — EducaDig ESG (Revisão TP3)

## 1. Problema de Negócio & Contexto
A falta de centralização e visibilidade sobre a infraestrutura tecnológica de escolas públicas no Brasil dificulta o direcionamento eficiente de recursos de investimento privado (ESG) e ações de ONGs. O **EducaDig ESG** visa solucionar essa fragmentação mapeando dados territoriais e analisando o cenário da inclusão digital sob o prisma do **ODS 4 (Educação de Qualidade)**.

Na fase **TP3**, a solução evolui de um painel isolado para uma **plataforma orientada a microsserviços/APIs**, integrando raspagem dinâmica de dados e preparando o terreno para análises avançadas com Inteligência Artificial Generativa (LLM).

---

## 2. Objetivos do Projeto (Atualizados - TP3)
* **Arquitetura Desmistificada:** Implementar uma API RESTful utilizando **FastAPI** para servir dados de ODS 4 e estatísticas da plataforma.
* **Interface Multipágina:** Reestruturar o aplicativo Streamlit em **múltiplas páginas nativas** (`pages/`), otimizando a experiência do usuário.
* **Scraping Híbrido:** Expandir a coleta de dados combinando **BeautifulSoup** (scraping estático) e **Selenium** (scraping dinâmico com renderização JavaScript/interações).
* **Preparação para LLM (TP4):** Estruturar os datasets textuais (`data/raw/*.txt`) para alimentar pipelines de RAG, Sumarização Automática e Análise de Sentimento na fase subsequente.

---

## 3. Escopo do Projeto

### Em Escopo (TP3):
1. **API Backend (FastAPI):**
   * Endpoint `GET /api/v1/noticias`: Consulta filtrada de artigos sobre ODS 4.
   * Endpoint `POST /api/v1/noticias`: Submissão de novas matérias para o dataset.
   * Endpoint `GET /api/v1/estatisticas`: Métricas consolidadas sobre os dados coletados.
   * Documentação interativa via Swagger UI (`/docs`).
2. **Frontend Multipágina (Streamlit):**
   * Página Home (Visão Geral & Métricas).
   * Página 1: Panorama Territorial (Dados IBGE).
   * Página 2: Notícias, Scraping & Nuvem de Palavras.
   * Página 3: Gestão de Dados, Upload e Persistência (`st.session_state`).
   * Página 4: Portal de Integração com a API FastAPI.
3. **Pipeline de Coleta de Dados:**
   * Script Selenium (`src/scraping_dynamic.py`) para navegação assíncrona.
   * Armazenamento estruturado na pasta `data/raw/`.

### Fora do Escopo (Adiado para TP4):
* Implementação dos prompts finais e conexão com APIs de LLM (OpenAI/Gemini/Ollama).
* Criação de banco de dados vetorial (Vector Database) para RAG.

---

## 4. Arquitetura Técnica & Tecnologias
* **Linguagem:** Python 3.10+
* **Frontend:** Streamlit (Multipage Architecture)
* **Backend / API:** FastAPI + Uvicorn
* **Scraping:** BeautifulSoup4, Requests & Selenium WebDriver
* **Processamento de Dados:** Pandas, NumPy
* **Visualização:** Matplotlib, WordCloud
* **Versionamento:** Git / GitHub

---

## 🟢 Declaração de Transparência (Uso de IA)
Em conformidade com as diretrizes do trabalho (**Sinal Verde 🟢**), declara-se que o código base das rotas do FastAPI, refatoração das páginas em Streamlit e estruturação desta documentação contaram com o suporte de Inteligência Artificial Generativa.