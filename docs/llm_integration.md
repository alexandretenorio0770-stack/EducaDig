## Integração de Modelo LLM Local e Arquitetura da API (TP4)

### 1. Identificação e Justificativa do Modelo Selecionado

* **Modelo Escolhido:** `pysentimiento/bertweet-pt-sentiment` (disponível no Hugging Face Model Hub).
* **Tarefa de NLP:** Classificação de texto e análise de polaridade editorial (`POS`, `NEU`, `NEG`) aplicada às notícias extraídas sobre Educação e Inclusão Digital (ODS 4).

#### Critérios de Seleção

| Critério | Avaliação Técnica no Projeto EducaDig ESG |
| :--- | :--- |
| **Desempenho** | Arquitetura baseada em RoBERTa/BERTweet pré-treinada especificamente em corpus de língua portuguesa. Apresenta alta precisão na distinção entre notícias factuais/descritivas (`NEU`) e conteúdos com carga positiva (`POS`) ou de alerta (`NEG`). |
| **Custo Computacional Local** | Modelo compacto (~440 MB), otimizado para execução em CPU comum sem exigência de GPU dedicada. Consome menos de 1,5 GB de memória RAM durante a inferência, processando requisições em milissegundos. |
| **Acessibilidade Local** | Carregado e executado integralmente no ambiente local através das bibliotecas `transformers` e `torch` (PyTorch CPU), eliminando dependência de APIs externas na nuvem, custos de tokens e riscos de privacidade após o download inicial. |

---

### 2. Arquitetura da Integração com FastAPI

A integração foi implementada no módulo `src/api_fastapi.py`, seguindo o fluxo abaixo:

1. **Carregamento no Ciclo de Vida (`@app.on_event("startup")`):** O pipeline do Hugging Face é inicializado uma única vez na subida do servidor, evitando recarregamentos a cada requisição HTTP e reduzindo a latência.
2. **Validação e Contratos (`Pydantic`):**
   * **Entrada (`TextoEntrada`):** Valida tamanho mínimo (10 caracteres) e máximo (2000 caracteres) do texto enviado.
   * **Saída (`ResultadoAnalise`):** Padroniza a resposta JSON com o texto original, tipo de análise, modelo utilizado, sigla da classificação, interpretação semântica e grau de confiança (`score`).
3. **Rota Principal (`POST /processar_texto`):** Recebe o payload JSON, aplica truncamento seguro de tokens (`max_length=512`) para proteção de memória e retorna a classificação estruturada.

---

### 3. Tratamento Robusto de Erros HTTP

Para assegurar resiliência e diagnósticos claros ao cliente, a API implementa exceções HTTP específicas (`HTTPException`):

* **`400 Bad Request`:** Retornado quando o texto enviado contém apenas espaços em branco ou não atinge o mínimo de caracteres válidos após limpeza.
* **`422 Unprocessable Entity`:** Validação automática de schema quando o JSON enviado não respeita os tipos ou limites definidos no modelo Pydantic.
* **`503 Service Unavailable`:** Retornado caso o modelo LLM local não tenha sido carregado corretamente na inicialização do servidor.
* **`500 Internal Server Error`:** Captura falhas inesperadas durante a inferência do modelo, devolvendo uma mensagem descritiva sem derrubar o serviço.

---

### 4. Declaração de Uso de Inteligência Artificial

Em conformidade com as diretrizes de integridade acadêmica da disciplina, declara-se que ferramentas de IA generativa (**Google Gemini**) foram utilizadas como suporte técnico para:
* Pesquisa comparativa de modelos leves de NLP em português no Hugging Face;
* Estruturação dos schemas de validação (`Pydantic`) e tratamento de exceções HTTP no FastAPI;
* Revisão e formatação desta documentação técnica.

Todo o código gerado foi validado, adaptado e testado localmente pelo autor no ambiente de desenvolvimento do projeto.