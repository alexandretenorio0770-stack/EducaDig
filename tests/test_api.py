import pytest
from fastapi.testclient import TestClient
from src.api_fastapi import app

@pytest.fixture(scope="module")
def client():
    # O bloco 'with' ativa o startup do FastAPI e carrega o modelo LLM local
    with TestClient(app) as c:
        yield c

def test_validacao_texto_muito_curto(client):
    """Garante que textos abaixo de 10 caracteres retornam erro 422 (Pydantic)."""
    response = client.post("/processar_texto", json={"texto": "Curto"})
    assert response.status_code == 422

def test_validacao_espacos_em_branco(client):
    """Garante que textos compostos apenas por espaços retornam erro 400."""
    response = client.post("/processar_texto", json={"texto": "               "})
    assert response.status_code == 400
    assert "caracteres válidos" in response.json()["detail"]

def test_fluxo_completo_classificacao_e_chat(client):
    """Testa inferência local e resposta do assistente conversacional."""
    resp_nlp = client.post(
        "/processar_texto",
        json={"texto": "Projeto leva internet gratuita e computadores para escolas rurais."}
    )
    assert resp_nlp.status_code == 200
    dados = resp_nlp.json()
    assert dados["sigla_classificacao"] in ["POS", "NEU", "NEG"]
    assert 0.0 <= dados["confianca"] <= 1.0

    resp_chat = client.post(
        "/chat_esg",
        json={"pergunta": "Quais iniciativas envolvem escolas e internet?", "historico": []}
    )
    assert resp_chat.status_code == 200
    assert "resposta" in resp_chat.json()