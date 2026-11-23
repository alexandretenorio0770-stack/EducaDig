# EducaDig ESG — Inteligência de Dados & IA Local para Educação (ODS 4)

Plataforma completa de **Ciência de Dados Aplicada e Inteligência Artificial Local** desenvolvida sob o framework **TDSP (Team Data Science Process)** para monitorar indicadores, notícias e políticas públicas voltadas à **Educação de Qualidade e Inclusão Digital (ODS 4 — Agenda 2030)**.

## Problema de Negócio & Impacto ESG

Organizações do terceiro setor, gestores públicos e áreas de sustentabilidade corporativa enfrentam dificuldades para acompanhar de forma estruturada e contínua o debate público e os gargalos de infraestrutura tecnológica nas escolas.

O **EducaDig ESG** resolve esse desafio automatizando o ciclo ponta a ponta:

* **Pilar Social (`S` do ESG) & ODS 4:** Transforma notícias dispersas e dados territoriais em evidências acionáveis para direcionar investimentos sociais privados (ISP) e ações de ONGs.
* **Governança (`G`) & Soberania de Dados:** Execução **100% local em CPU**, sem envio de informações para APIs externas pagas, com contratos validados via `Pydantic` e testes automatizados (`Pytest`).
* **Green AI (Eficiência Computacional):** Utiliza modelos leves e otimizados (`pysentimiento/bertweet-pt-sentiment` + `TF-IDF`), reduzindo consumo energético e custo operacional.

## Arquitetura e Estrutura do Projeto

```text
EducaDig/
├── app/
│   └── pages/
│       ├── panorama.py          # Dados territoriais (API IBGE) e contexto ODS 4
│       ├── noticias.py          # Nuvem de palavras (NLP) e base coletada
│       ├── gestao.py            # Orquestração ETL (Selenium + Classificação IA em Lote)
│       ├── consumoAPI.py        # Testes diretos dos endpoints GET e POST
│       └── assistente_ia.py     # Classificador individual e Chat ESG com memória
├── data/
│   ├── raw/                     # Dados brutos extraídos (noticias_esg.csv)
│   └── processed/               # Base enriquecida com polaridade e confiança
├── docs/
│   ├── project_charter.md       # Escopo, objetivos e declaração de uso de IA (TDSP)
│   └── data_summary_report.md   # Dicionário de dados, limpeza e pipeline
├── src/
│   ├── api.py                   # Integração com a API pública do IBGE
│   ├── api_fastapi.py           # Backend REST (FastAPI + Hugging Face + Mini-RAG)
│   └── scraping_dynamic.py      # Coleta automatizada com Selenium
├── tests/
│   └── test_api.py              # Testes automatizados de contrato e inferência (Pytest)
├── main.py                      # Ponto de entrada multipágina (st.navigation)
├── Procfile                     # Orquestração simultânea de Backend e Frontend
└── requirements.txt             # Dependências do projeto
```

## Funcionalidades Principais

1. **Coleta Automatizada (Web Scraping Dinâmico):** Extração de notícias reais do *Observatório do Terceiro Setor* utilizando `Selenium`, disparável tanto via terminal quanto diretamente pela interface web.
2. **Enriquecimento em Lote & Classificação NLP (`FastAPI` + `Hugging Face`):**
   * Classificação de polaridade editorial (`POS`, `NEU`, `NEG`) e score de confiança usando o modelo `pysentimiento/bertweet-pt-sentiment`.
   * Processamento individual (`POST /processar_texto`) e em lote (`POST /processar_lote`), salvando o dataset enriquecido em `data/processed/noticias_classificadas.csv`.
3. **Assistente Conversacional ESG com Mini-RAG (`POST /chat_esg`):**
   * Mantém o histórico da conversa na sessão (`st.session_state`).
   * Combina **TF-IDF + Similaridade de Cosseno (`scikit-learn`)** para recuperar as notícias mais relevantes da base local e diagnosticar o impacto sob a ótica do ODS 4.
   * Permite exportar o relatório completo da sessão em `.txt` e a base classificada em `.csv`.
4. **Visualização Analítica (`Streamlit`):** Navegação multipágina moderna (`st.navigation`) com gráficos de distribuição de sentimentos, nuvem de palavras com filtragem de *stopwords* e tabelas interativas.

## Como Executar o Projeto Localmente

### 1. Clonar o repositório e ativar o ambiente virtual

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd EducaDig
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Executar Backend e Frontend juntos (via `Procfile` + `honcho`)

```bash
.\.venv\Scripts\python.exe -m honcho start
```

*(Alternativamente, você pode rodar em dois terminais separados: `uvicorn src.api_fastapi:app --port 8000` e `streamlit run main.py`).*

### 3. Acessar as interfaces

* **Dashboard Streamlit:** `http://localhost:8501`
* **Documentação Interativa da API (Swagger):** `http://127.0.0.1:8000/docs`

## Testes Automatizados

Para validar os contratos `Pydantic`, o tratamento de erros HTTP (`400`, `422`, `503`) e a inferência do modelo local:

```bash
.\.venv\Scripts\python.exe -m pytest
```

## Declaração de Integridade Acadêmica e Uso de IA

Em conformidade com as diretrizes do Projeto de Bloco, registra-se que ferramentas de Inteligência Artificial Generativa (**Google Gemini**) foram utilizadas como apoio técnico para pesquisa de modelos pré-treinados leves na Hugging Face, estruturação dos endpoints FastAPI/Pydantic, implementação da busca vetorial TF-IDF e revisão da documentação TDSP. Todo o código e os artefatos foram integrados, testados e validados localmente pelo autor.