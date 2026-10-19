from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()
df = pd.read_csv('data\\raw\\noticias_esg.csv')

class Noticia(BaseModel):
    titulo: str
    link: str

@app.get("/")
def ler_raiz():
    return {"status": "Servidor ativo", "projeto": "EducaDig"}

@app.get('/api/v1/noticias')
async def noticias():
    df_limpo = df.copy()
    df_limpo['titulo'] = df_limpo['titulo'].fillna("Sem Título")
    return {'df': df_limpo.to_dict(orient='records')}

@app.post("/api/v1/noticias", status_code=201)
def criar_noticia(noticia: Noticia):
    nova_linha = pd.DataFrame([{
        "titulo": noticia.titulo,
        "link": noticia.link
    }])

    try:
        nova_linha.to_dict(df, mode='a', header=False, index=False)
        
        return {"status": "sucesso", "mensagem": "Notícia adicionada!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar: {str(e)}")