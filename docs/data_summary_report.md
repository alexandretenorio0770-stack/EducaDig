# 📊 Data Summary Report — EducaDig ESG (Revisão TP3)

## 1. Resumo das Fontes de Dados

O projeto **EducaDig ESG** combina dados estruturados de APIs governamentais com dados não estruturados e semi-estruturados coletados via Web Scraping estático e dinâmico.

| Fonte | Tipo de Fonte | Método de Extração | Formato Final | Frequência / Uso |
| :--- | :--- | :--- | :--- | :--- |
| **IBGE (API Localidades)** | API REST Pública | Requisições HTTP (`requests`) | DataFrame / Session | Dados de municípios do estado de São Paulo |
| **Observatório do Terceiro Setor** | Web Page Estática | `BeautifulSoup4` (`src/scraping.py`) | CSV / TXT | Notícias e artigos focados em ODS 4 |
| **Portais de Notícias ESG** | Web Page Dinâmica | `Selenium` (`src/scraping_dynamic.py`) | CSV / TXT | Conteúdo com carregamento assíncrono / JS |
| **FastAPI Backend** | API Interna REST | Endpoints HTTP (`src/api_fastapi.py`) | JSON / Dataframe | Consumo e cadastro centralizado de dados |

---

## 2. Estrutura dos Arquivos de Dados (`data/raw/`)

### A. `data/raw/noticias_esg.csv`
Armazena a listagem de matérias capturadas pelos scripts de scraping.
* **Campos:** `titulo`, `link`, `data_publicacao`, `resumo`, `fonte`.
* **Utilização:** Exibição no Streamlit, filtros na API FastAPI e input para futura classificação por LLM.

### B. `data/raw/texto_esg.txt`
Arquivo consolidado com o corpo de texto de todos os artigos extraídos.
* **Estrutura:** Texto corrido limpo de caracteres especiais e tags HTML.
* **Utilização:** Geração da Nuvem de Palavras (`WordCloud`) e preparação de *chunks* de texto para tarefas de RAG/Sumarização na etapa de LLM.

---

## 3. Estratégia de Preparação para IA e LLMs (Visão TP4)

Para garantir uma transição fluida para a próxima fase do projeto, os dados coletados no TP3 foram preparados estrategicamente para os seguintes casos de uso com LLMs:

1. **Sumarização Executiva (Text Summarization):**
   * *Dataset:* `texto_esg.txt` / `noticias_esg.csv`.
   * *Aplicação:* Condensar longas matérias sobre políticas públicas e editais em boletins curtos para tomada de decisão ESG.

2. **Análise de Sentimentos e Impacto:**
   * *Dataset:* `titulos` e `resumos` das notícias.
   * *Aplicação:* Classificar o tom das notícias (ex: "Crítico - Falta de Infraestrutura", "Positivo - Investimento Realizado", "Neutro") para medir o índice de urgência regional.

3. **Sistema de Perguntas e Respostas (RAG - Question Answering):**
   * *Dataset:* Corpus textual acumulado na pasta `data/`.
   * *Aplicação:* Permitir que gestores perguntem à plataforma: *"Quais foram os principais desafios de conectividade relatados nas escolas públicas em 2026?"*.