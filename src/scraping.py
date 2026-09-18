import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def raspar_noticias_esg():
    url_lista = "https://observatorio3setor.org.br/ods/ods-04/"
    resposta = requests.get(url_lista, headers=HEADERS)
    
    if resposta.status_code != 200:
        print("Falha ao acessar o site.")
        return

    soup = BeautifulSoup(resposta.content, "html.parser")
    
    artigos = soup.find_all("article", limit=5)  # Coleta as 5 primeiras matérias
    
    dados_coletados = []

    for artigo in artigos:
        tag_link = artigo.find("a")
        if not tag_link:
            continue
            
        titulo = tag_link.get_text(strip=True)
        link_materia = tag_link.get("href")


        resposta_materia = requests.get(link_materia, headers=HEADERS)
        soup_materia = BeautifulSoup(resposta_materia.content, "html.parser")

        container_texto = soup_materia.find("div", class_="entry-content")
        
        if container_texto:
            paragrafos = container_texto.find_all("p")

            texto_completo = " ".join([p.get_text(strip=True) for p in paragrafos])
        else:
            texto_completo = "Conteúdo não localizado."

        dados_coletados.append({
            "titulo": titulo,
            "link": link_materia,
            "conteudo": texto_completo
        })

    os.makedirs("data/raw", exist_ok=True)
    df = pd.DataFrame(dados_coletados)

    df.to_csv("data/raw/noticias_esg.csv", index=False, encoding="utf-8-sig")
    
    todos_os_textos = " ".join(df["conteudo"].tolist())
    with open("data/raw/texto_esg.txt", "w", encoding="utf-8") as f:
        f.write(todos_os_textos)

    print("Scraping concluído! Arquivos salvos em data/raw/")

if __name__ == "__main__":
    raspar_noticias_esg()