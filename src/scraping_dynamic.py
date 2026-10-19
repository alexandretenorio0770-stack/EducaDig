import os
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def executar_scraping_dinamico():
    print("A iniciar o WebDriver do Selenium...")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        url = "https://observatorio3setor.org.br/ods/ods-04/" 
        print(f"A aceder a: {url}")
        driver.get(url)

        print("A aguardar o carregamento dos elementos dinâmicos...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article"))
        )

        elementos_artigos = driver.find_elements(By.CSS_SELECTOR, "article")
        dados_recolhidos = []

        print(f"Foram encontrados {len(elementos_artigos)} elementos. A extrair dados...")

        for artigo in elementos_artigos:
            try:

                titulo_elem = artigo.find_element(By.CSS_SELECTOR, "h2, h3")
                link_elem = artigo.find_element(By.CSS_SELECTOR, "a")
                
                titulo = titulo_elem.text.strip()
                link = link_elem.get_attribute("href")

                if titulo and link:
                    dados_recolhidos.append({
                        "titulo": titulo,
                        "link": link
                    })
            except Exception as e:
                continue

        os.makedirs("data/raw", exist_ok=True)

        if dados_recolhidos:
            df = pd.DataFrame(dados_recolhidos)
            raiz_projeto = Path(__file__).resolve().parent.parent
            pasta_destino = raiz_projeto / "data" / "raw"
            pasta_destino.mkdir(parents=True, exist_ok=True)

            caminho_ficheiro = pasta_destino / "noticias_esg.csv"
            df.to_csv(caminho_ficheiro, index=False, encoding="utf-8")
            print(f"Sucesso! {len(dados_recolhidos)} registos guardados em '{caminho_ficheiro}'.")

    except Exception as erro:
        print(f"Ocorreu um erro durante a execução do Selenium: {erro}")

    finally:
        driver.quit()
        print("Sessão do Selenium encerrada.")

if __name__ == "__main__":
    executar_scraping_dinamico()