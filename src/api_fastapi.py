import os
os.environ["HF_HOME"] = "C:\\hf_cache"
os.environ["TRANSFORMERS_CACHE"] = "C:\\hf_cache"

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- CAMINHOS DO PROJETO ---
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_RAW = RAIZ_PROJETO / "data" / "raw" / "noticias_esg.csv"
PASTA_PROCESSED = RAIZ_PROJETO / "data" / "processed"
CAMINHO_PROCESSED = PASTA_PROCESSED / "noticias_classificadas.csv"

# ==============================================================================
# BLOCO DE CARREGAMENTO DO MODELO LLM LOCAL (INÍCIO)
# ==============================================================================
MODELO_NOME = "pysentimiento/bertweet-pt-sentiment"
analisador_nlp = None

def obter_modelo():
    """Carrega o modelo na memória (no startup ou sob demanda na 1ª requisição)."""
    global analisador_nlp
    if analisador_nlp is None:
        logger.info(f"Carregando modelo local: {MODELO_NOME}...")
        analisador_nlp = pipeline("sentiment-analysis", model=MODELO_NOME)
        logger.info("Modelo carregado com sucesso!")
    return analisador_nlp

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        obter_modelo()
    except Exception as e:
        logger.error(f"Falha no startup ao carregar modelo: {e}")
    yield
    global analisador_nlp
    analisador_nlp = None

app = FastAPI(
    title="EducaDig ESG API - Enterprise Local",
    description="API local com ETL em lote, NLP (Hugging Face) e RAG leve (TF-IDF) para monitoramento ESG/ODS 4.",
    version="4.0.0",
    lifespan=lifespan
)
# ==============================================================================
# BLOCO DE CARREGAMENTO DO MODELO LLM LOCAL (FIM)
# ==============================================================================

MAPA_SENTIMENTOS = {
    "POS": "Positivo (Impacto favorável / Avanço no ODS 4)",
    "NEU": "Neutro (Informativo / Descritivo)",
    "NEG": "Negativo (Alerta / Desafio ou déficit educacional)"
}

# --- SCHEMAS PYDANTIC ---
class TextoEntrada(BaseModel):
    texto: str = Field(..., min_length=10, max_length=2000)

class ResultadoAnalise(BaseModel):
    texto_analisado: str
    tipo_analise: str
    modelo_utilizado: str
    sigla_classificacao: str
    interpretacao: str
    confianca: float

class ResumoLote(BaseModel):
    mensagem: str
    total_processado: int
    distribuicao: dict
    arquivo_salvo: str

class MensagemChat(BaseModel):
    role: str
    content: str

class ChatEntrada(BaseModel):
    pergunta: str = Field(..., min_length=3)
    historico: List[MensagemChat] = []

class ChatResposta(BaseModel):
    resposta: str
    total_noticias_base: int
    noticias_relacionadas: List[str]
    polaridade_consulta: str

# --- ROTA 1: LISTAGEM DE NOTÍCIAS ---
@app.get("/noticias", status_code=status.HTTP_200_OK)
def listar_noticias():
    caminho = CAMINHO_PROCESSED if CAMINHO_PROCESSED.exists() else CAMINHO_RAW
    if not caminho.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhuma base de notícias encontrada. Execute o scraping primeiro."
        )
    df = pd.read_csv(caminho).fillna("")
    return {"fonte": caminho.name, "total": len(df), "dados": df.to_dict(orient="records")}

# --- ROTA 2: CLASSIFICAÇÃO INDIVIDUAL ---
@app.post("/processar_texto", response_model=ResultadoAnalise, status_code=status.HTTP_200_OK)
def processar_texto(payload: TextoEntrada):
    texto_limpo = payload.texto.strip()
    if len(texto_limpo) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O texto precisa ter ao menos 10 caracteres válidos."
        )

    try:
        modelo = obter_modelo()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Falha ao carregar modelo LLM local: {str(e)}"
        )

    try:
        predicao = modelo(texto_limpo, truncation=True, max_length=512)[0]
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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {str(e)}")

# --- ROTA 3: ENRIQUECIMENTO EM LOTE (ETL + IA) ---
@app.post("/processar_lote", response_model=ResumoLote, status_code=status.HTTP_200_OK)
def processar_lote():
    if not CAMINHO_RAW.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Arquivo data/raw/noticias_esg.csv não encontrado.")

    try:
        modelo = obter_modelo()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Falha ao carregar modelo LLM local: {str(e)}"
        )

    try:
        df = pd.read_csv(CAMINHO_RAW).fillna("")
        if df.empty:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O CSV bruto está vazio.")

        coluna_texto = df.columns[0]
        textos = df[coluna_texto].astype(str).tolist()

        predicoes = modelo(textos, truncation=True, max_length=512)
        df["sentimento"] = [p["label"] for p in predicoes]
        df["interpretacao"] = [MAPA_SENTIMENTOS.get(p["label"], p["label"]) for p in predicoes]
        df["confianca"] = [round(float(p["score"]), 4) for p in predicoes]

        PASTA_PROCESSED.mkdir(parents=True, exist_ok=True)
        df.to_csv(CAMINHO_PROCESSED, index=False, encoding="utf-8")

        contagem = df["sentimento"].value_counts().to_dict()

        return ResumoLote(
            mensagem="Base enriquecida com sucesso pelo modelo LLM local.",
            total_processado=len(df),
            distribuicao=contagem,
            arquivo_salvo=str(CAMINHO_PROCESSED.relative_to(RAIZ_PROJETO))
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Falha no processamento em lote: {str(e)}")

# --- ROTA 4: ASSISTENTE CONVERSACIONAL COM MINI-RAG (TF-IDF + COSINE SIMILARITY) ---
@app.post("/chat_esg", response_model=ChatResposta, status_code=status.HTTP_200_OK)
def chat_esg(payload: ChatEntrada):
    try:
        modelo = obter_modelo()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Falha ao carregar modelo LLM local: {str(e)}"
        )

    caminho_base = CAMINHO_PROCESSED if CAMINHO_PROCESSED.exists() else CAMINHO_RAW
    noticias_texto = []
    if caminho_base.exists():
        df = pd.read_csv(caminho_base).fillna("")
        if not df.empty:
            coluna_texto = df.columns[0]
            noticias_texto = df[coluna_texto].astype(str).tolist()

    ultimas_perguntas = [m.content for m in payload.historico[-3:] if m.role == "user"]
    consulta_contextual = " ".join(ultimas_perguntas + [payload.pergunta]).strip()

    relacionadas = []
    if noticias_texto:
        try:
            vetorizador = TfidfVectorizer()
            matriz_tfidf = vetorizador.fit_transform(noticias_texto + [consulta_contextual])
            similaridades = cosine_similarity(matriz_tfidf[-1], matriz_tfidf[:-1]).flatten()
            indices_top = similaridades.argsort()[::-1]

            relacionadas = [noticias_texto[i] for i in indices_top if similaridades[i] > 0.05][:4]
            if not relacionadas:
                relacionadas = [noticias_texto[i] for i in indices_top[:3]]
        except Exception:
            relacionadas = noticias_texto[:3]

    predicao = modelo(payload.pergunta, truncation=True, max_length=512)[0]
    tom = MAPA_SENTIMENTOS.get(predicao["label"], predicao["label"])

    qtd_turnos = len([m for m in payload.historico if m.role == "user"])
    ref_memoria = f"Considerando o histórico da nossa conversa ({qtd_turnos} turno(s) anterior(es)), " if qtd_turnos > 0 else ""

    if relacionadas:
        lista_formatada = "\n".join([f"- *{item}*" for item in relacionadas])
        resposta_texto = (
            f"{ref_memoria}realizei uma busca semântica na base de **{len(noticias_texto)} notícias** do Observatório do Terceiro Setor.\n\n"
            f"**Evidências mais relevantes encontradas:**\n{lista_formatada}\n\n"
            f"**Diagnóstico ESG / ODS 4:** O enfoque da sua consulta apresenta tom **{tom}**. "
            f"Esses registros servem como insumo direto para relatórios de impacto e governança educacional."
        )
    else:
        resposta_texto = (
            f"{ref_memoria}nenhuma notícia foi encontrada na base local. Dispare a coleta via Selenium na página de Gestão de Dados."
        )

    return ChatResposta(
        resposta=resposta_texto,
        total_noticias_base=len(noticias_texto),
        noticias_relacionadas=relacionadas,
        polaridade_consulta=tom
    )