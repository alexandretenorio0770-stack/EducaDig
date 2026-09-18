# EducaDig ESG — Mapeamento de Inclusão Digital Escolar (ODS 4)

Projeto desenvolvido para a disciplina de Desenvolvimento de Soluções Sustentáveis com ESG e Agenda 2030 (TP1).

## Estrutura do Projeto (TDSP)
- `app/`: Aplicação Streamlit (Interface).
- `src/`: Módulos de coleta e tratamento de dados (APIs).
- `docs/`: Artefatos de gestão (Project Charter e Data Summary Report).
- `requirements.txt`: Dependências do projeto.

## Como Executar
1. Clone o repositório.
2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
3. Executar o Web Scraping (Geração de Dados)
    ```
    python src/scraping.py
    ```
4. Executar a Aplicação Streamlit
   ```
   streamlit run app/main.py
   ```  