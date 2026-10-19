import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def executar_scraping_dinamico():
    print("A iniciar o WebDriver do Selenium...")
    
    # Configurar o Selenium para rodar em modo 'headless' (sem abrir a janela gráfica visível)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Inicializar o navegador
    driver = webdriver.Chrome(options=options)

    try:
        # Substitua pela URL real do site que pretende raspar
        url = "https://observatorio3setor.org.br/" 
        print(f"A aceder a: {url}")
        driver.get(url)

        # 1. Esperar explicitamente até que os artigos/elementos carreguem na página (evita erros de carregamento assíncrono)
        # Nota: Ajuste o seletor CSS (ex: "article", ".post-item", etc.) conforme a estrutura do site alvo
        print("A aguardar o carregamento dos elementos dinâmicos...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article"))
        )

        # 2. Localizar os elementos na página
        elementos_artigos = driver.find_elements(By.CSS_SELECTOR, "article")
        dados_recolhidos = []

        print(f"Foram encontrados {len(elementos_artigos)} elementos. A extrair dados...")

        for artigo in elementos_artigos:
            try:
                # Extrair o título (procura por h2 ou h3 dentro do artigo)
                titulo_elem = artigo.find_element(By.CSS_SELECTOR, "h2, h3")
                # Extrair o link associado
                link_elem = artigo.find_element(By.CSS_SELECTOR, "a")
                
                titulo = titulo_elem.text.strip()
                link = link_elem.get_attribute("href")

                if titulo and link:
                    dados_recolhidos.append({
                        "titulo": titulo,
                        "link": link
                    })
            except Exception as e:
                # Ignora elementos que não tenham a estrutura esperada e continua
                continue

        # 3. Garantir que a pasta de destino existe
        os.makedirs("data/raw", exist_ok=True)

        # 4. Gravar os dados recolhidos num ficheiro CSV utilizando o Pandas
        if dados_recolhidos:
            df = pd.DataFrame(dados_recolhidos)
            caminho_ficheiro = "data/raw/noticias_esg.csv"
            
            # Guarda o ficheiro para ser consumido pelo Streamlit
            df.to_csv(caminho_ficheiro, index=False, encoding="utf-8")
            print(f"Sucesso! {len(dados_recolhidos)} registos guardados em '{caminho_ficheiro}'.")
        else:
            print("Nenhum dado foi recolhido. Verifique se os seletores CSS correspondem à página.")

    except Exception as erro:
        print(f"Ocorreu um erro durante a execução do Selenium: {erro}")

    finally:
        # Fechar o navegador e terminar a sessão do driver
        driver.quit()
        print("Sessão do Selenium encerrada.")

if __name__ == "__main__":
    executar_scraping_dinamico()