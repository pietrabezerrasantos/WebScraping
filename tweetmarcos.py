from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import csv
import time
import os
from datetime import datetime

TWITTER_USER = "gracieabrams"  
MAX_TWEETS   = 10             
OUTPUT_FILE  = "tweets.csv"
SCROLL_PAUSE = 2.0             
PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CAMINHO_CSV  = os.path.join(PASTA_SCRIPT, OUTPUT_FILE)

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--lang=pt-BR")
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

def extrair_campo(elemento, seletor, atributo=None):
    """Tenta extrair um campo; retorna '' se nao encontrar."""
    try:
        el = elemento.find_element(By.CSS_SELECTOR, seletor)
        return el.get_attribute(atributo) if atributo else el.text.strip()
    except NoSuchElementException:
        return ""
    
def scrape_tweets(driver, username, max_tweets):
    url = f"https://twitter.com/{username}"
    print(f"Acessando perfil: {url}")
    driver.get(url)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "article[data-testid='tweet']"))
    )

    coletados = {}  

    print(f"Coletando ate {max_tweets} tweets...\n")

    while len(coletados) < max_tweets:
        artigos = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='tweet']")

        for artigo in artigos:
            if len(coletados) >= max_tweets:
                break

            autor_nome    = extrair_campo(artigo, "[data-testid='User-Name'] span")
            autor_handle  = extrair_campo(artigo, "[data-testid='User-Name'] a", "href")
            texto         = extrair_campo(artigo, "[data-testid='tweetText']")
            data_iso      = extrair_campo(artigo, "time", "datetime")
            link_tweet    = extrair_campo(artigo, "a[href*='/status/']", "href")
            curtidas      = extrair_campo(artigo, "[data-testid='like'] span")
            retweets      = extrair_campo(artigo, "[data-testid='retweet'] span")
            respostas     = extrair_campo(artigo, "[data-testid='reply'] span")
            visualizacoes = extrair_campo(artigo, "a[href*='/analytics'] span")
            midia         = "Sim" if artigo.find_elements(
                               By.CSS_SELECTOR, "[data-testid='tweetPhoto'], video") else "Nao"

            data_fmt = ""
            if data_iso:
                try:
                    dt = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))
                    data_fmt = dt.strftime("%d/%m/%Y %H:%M")
                except ValueError:
                    data_fmt = data_iso

            chave = link_tweet or texto[:60]
            if chave and chave not in coletados:
                coletados[chave] = {
                    "autor_nome":    autor_nome,
                    "autor_handle":  autor_handle.lstrip("/") if autor_handle else "",
                    "texto":         texto,
                    "data":          data_fmt,
                    "data_iso":      data_iso,
                    "curtidas":      curtidas      or "0",
                    "retweets":      retweets      or "0",
                    "respostas":     respostas     or "0",
                    "visualizacoes": visualizacoes or "0",
                    "tem_midia":     midia,
                    "link":          f"https://twitter.com{link_tweet}" if link_tweet else "",
                }
                print(f"  [{len(coletados):>3}/{max_tweets}] {data_fmt} — {texto[:70]}...")

        altura_antes = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE)
        altura_depois = driver.execute_script("return document.body.scrollHeight")

        if altura_depois == altura_antes:
            print("\nFim da pagina — nao ha mais tweets para carregar.")
            break

    return list(coletados.values())


def salvar_csv(tweets, caminho):
    if not tweets:
        print("Nenhum tweet para salvar.")
        return

    campos = [
        "autor_nome", "autor_handle", "texto", "data", "data_iso",
        "curtidas", "retweets", "respostas", "visualizacoes",
        "tem_midia", "link"
    ]

    with open(caminho, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(tweets)

    print(f"\n{len(tweets)} tweets salvos em:\n{caminho}")

if __name__ == "__main__":
    driver = init_driver()
    try:
        tweets = scrape_tweets(driver, TWITTER_USER, MAX_TWEETS)
        salvar_csv(tweets, CAMINHO_CSV)
    finally:
        driver.quit()
