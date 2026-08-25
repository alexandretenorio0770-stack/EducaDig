# Data Summary Report — EducaDig ESG

## 1. Visão Geral das Fontes de Dados
Este documento descreve as fontes de dados primárias e secundárias que compõem o ecossistema da aplicação EducaDig ESG.

## 2. Fontes de Dados Atuais (Fase TP1)
* **Fonte:** API de Localidades do IBGE (Instituto Brasileiro de Geografia e Estatística).
* **URL / Endpoint:** `https://servicodados.ibge.gov.br/api/v1/localidades/estados/35/municipios`
* **Tipo de Dado:** Estruturado (JSON via HTTP GET).
* **Objetivo de Uso:** Mapear a hierarquia territorial (Município, Microrregião e Mesorregião) do Estado de São Paulo para servir de dimensão geográfica e chave de cruzamento.

## 3. Fontes de Dados Futuras (Próximas Fases)
* **Censo Escolar / INEP (Dados Abertos):** Indicadores de infraestrutura (acesso à internet, laboratórios de informática, computadores por aluno).
* **Tipo de Dado:** CSV / API REST.
* **Objetivo de Uso:** Calcular o índice de vulnerabilidade de inclusão digital por escola/município.