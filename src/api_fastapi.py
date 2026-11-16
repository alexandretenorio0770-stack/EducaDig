from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from transformers import pipeline
from pathlib import Path
import pandas as pd
import logging

# Configuração de logs para acompanhamento no terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="EducaDig ESG API - TP4",
    description="API local com FastAPI e HuggingFace para monitoramento e análise de sentimentos sobre ODS 4.",
    version="2.0.0"
)

# --- CAMINHOS DO PROJETO ---
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_CSV = RAIZ_PROJETO / "data" / "raw" / "noticias_esg.csv"

# --- CONFIGURAÇÃO DO MODELO LLM LOCAL ---
MODELO_NOME = "pysentimiento/bertweet-pt-sentiment"
analisador_nlp = None

MAPA_SENTIMENTOS = {
    "POS": "Positivo (Impacto favorável / Avanço no ODS 4)",
    "NEU": "Neutro (Informativo / Descritivo)",
    "NEG": "Negativo (Alerta / Desafio ou déficit educacional)"
}

@app.on_event("startup")
def carregar_modelo_local():
    global analisador_nlp
    try:
        logger.info(f"Iniciando download/carregamento local do modelo: {MODELO_NOME}...")
        analisador_nlp = pipeline("sentiment-analysis", model=MODELO_NOME)
        logger.info("Modelo LLM carregado na memória com sucesso!")
    except Exception as e:
        logger.error(f"Erro crítico ao carregar o modelo local: {e}")
        analisador_nlp = None

# --- SCHEMAS PYDANTIC (VALIDAÇÃO E RESPONSE MODELS) ---
class TextoEntrada(BaseModel):
    texto: str = Field(
        ..., 
        min_length=10, 
        max_length=2000,
        description="Título ou trecho da notícia sobre educação/ESG para análise.",
        examples=["Novas escolas públicas recebem laboratórios de informática e internet de alta velocidade."]
    )

class ResultadoAnalise(BaseModel):
    texto_analisado: str
    tipo_analise: str
    modelo_utilizado: str
    sigla_classificacao: str
    interpretacao: str
    confianca: float

# --- ROTAS DO TP3 (CONSULTA AOS DADOS EXTRAÍDOS) ---
@app.get("/noticias", status_code=status.HTTP_200_OK)
def listar_noticias():
    if not CAMINHO_CSV.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Base de dados não encontrada. Execute o script de scraping primeiro."
        )
    df = pd.read_csv(CAMINHO_CSV)
    return {"total": len(df), "dados": df.to_dict(orient="records")}

# --- ROTA DO TP4 (PROCESSAMENTO COM LLM LOCAL) ---
@app.post("/processar_texto", response_model=ResultadoAnalise, status_code=status.HTTP_200_OK)
def processar_texto(payload: TextoEntrada):
    # 1. Erro 503: Falha no carregamento do modelo
    if analisador_nlp is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="O modelo LLM local não está carregado. Verifique a conexão inicial para download ou os logs do servidor."
        )

    # 2. Erro 400: Entrada vazia após limpeza
    texto_limpo = payload.texto.strip()
    if len(texto_limpo) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O texto enviado precisa ter pelo menos 10 caracteres válidos após remoção de espaços."
        )

    # 3. Inferência local com tratamento de exceções (Erro 500)
    try:
        # Modelos BERT têm limite de 512 tokens; truncamos por segurança de memória
        predicao = analisador_nlp(texto_limpo, truncation=True, max_length=512)[0]
        sigla = predicao["label"]
        score = round(float(predicao["score"]), 4)

        return ResultadoAnalise(
            texto_analisado=texto_limpo,
            tipo_analise="Análise de Sentimento / Tom Editorial (ODS 4)",
            modelo_utilizado=MODELO_NOME,
            sigla_classificacao=sigla,
            interpretacao=MAPA_SENTIMENTOS.get(sigla, sigla),
            confianca=score
        )
    except Exception as e:
        logger.error(f"Erro durante a inferência: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha interna ao processar o texto no modelo local: {str(e)}"
        )