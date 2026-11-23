# Project Charter — EducaDig ESG (Consolidação Final)

## 1. Problema de Negócio e Alinhamento ESG / ODS
Organizações do terceiro setor, gestores públicos e áreas de sustentabilidade corporativa enfrentam dificuldades para acompanhar, de forma estruturada e contínua, o volume de notícias e indicadores sobre **Educação de Qualidade e Inclusão Digital (ODS 4 da Agenda 2030)**.

O **EducaDig ESG** resolve esse problema entregando uma plataforma local de Ciência de Dados Aplicada que automatiza a coleta de notícias do setor social, extrai padrões temáticos e utiliza Processamento de Linguagem Natural (NLP) para classificar o tom editorial e apoiar consultas analíticas.

## 2. Arquitetura da Solução e Ciclo de Ciência de Dados
A solução foi desenhada seguindo o framework **TDSP (Team Data Science Process)**, cobrindo o ciclo ponta a ponta:

* **Coleta & Engenharia de Dados:** Extração automatizada com Selenium e armazenamento estruturado em CSV com caminhos independentes de diretório (`pathlib`).
* **Análise Exploratória & Visualização:** Dashboard multipágina em Streamlit (`st.navigation`) exibindo panorama territorial, gestão dos dados coletados e nuvem de palavras filtrada.
* **Modelagem & Inteligência Artificial Local:** Integração do modelo `pysentimiento/bertweet-pt-sentiment` (Hugging Face) via FastAPI, rodando 100% em CPU local, com contratos validados por `Pydantic` e tratamento robusto de exceções HTTP (`400`, `404`, `422`, `500`, `503`).
* **Solução Conversacional (Memória de Sessão):** Implementação de um Consultor ESG (`POST /chat_esg` + `st.session_state`) que mantém o histórico de interações do usuário e cruza perguntas em linguagem natural com as notícias reais da base de dados.

## 3. Benefícios e Impacto para Tomada de Decisão
* **Soberania e Baixo Custo Computacional:** Execução integralmente local (~440 MB), sem custos de APIs externas ou envio de dados sensíveis para terceiros.
* **Agilidade Analítica:** Reduz o tempo de leitura manual de portais de notícias, destacando imediatamente avanços (`POS`), fatos descritivos (`NEU`) e pontos de alerta (`NEG`) ligados à educação.

## 4. Declaração de Uso de Inteligência Artificial
Em conformidade com as diretrizes de integridade acadêmica da disciplina, registra-se que ferramentas de IA generativa (**Google Gemini**) foram utilizadas como suporte técnico para pesquisa de modelos leves na Hugging Face, estruturação dos endpoints FastAPI/Pydantic, integração da memória conversacional no Streamlit e revisão da documentação do TDSP. Todo o código e os artefatos foram adaptados, executados e validados localmente pelo autor.