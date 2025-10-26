from fastapi import FastAPI, Query
from typing import List
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="News Scraper API",
    description="API simples para buscar notícias relacionadas à indústria avícola na CNN Brasil.",
    version="1.0.0"
)

# Lista padrão de palavras-chave
DEFAULT_KEYWORDS = [
    "indústria avícola", "processamento de frango", "frigorífico", "exportação de frango",
    "importação de frango", "mercado avícola", "preço do frango", "custos industriais",
    # "cadeia produtiva", "produção intensiva", "automação industrial", "logística avícola",
    # "qualidade da carne", "normas sanitárias", "inspeção federal", "certificação de alimentos",
    # "SIF", "selo SIF", "vistorias SIF", "inovação tecnológica", "biotecnologia avícola",
    # "indústria de alimentos", "produção industrial", "processamento de carne", "abate industrial",
    # "estocagem frigorífica", "distribuição de frango", "armazenamento a frio", "exportação de ovos",
    # "indústria de ovos", "embalagem de frango", "rotulagem de alimentos", "industria alimentícia",
    # "produção em larga escala", "controle de qualidade", "mercado internacional", "exportadores de frango",
    # "investimentos industriais", "sustentabilidade industrial", "impacto ambiental", "normas ISO",
    # "gestão de produção", "automatização de linha de produção", "processamento de cortes",
    # "industrialização do frango", "cadeia logística", "indústria de proteína animal",
    # "produção de alimentos processados", "tecnologia de abate", "engenharia de alimentos",
    # "segurança alimentar", "regulamentação avícola", "granjas comerciais", "produção de pintinhos",
    # "alimentação de frangos", "sanidade avícola"
]

# Sites para busca
WEBSITES = [{
    "https://www.cnnbrasil.com.br": 
    "https://www.cnnbrasil.com.br/?search={search}&orderby=date&order=desc"
}]


def search_articles(keywords: List[str], websites: List[dict[str, str]]):
    relevant_news = []

    for website in websites:
        for default_url, search_url in website.items():
            for keyword in keywords:
                formatted_url = search_url.format(search=keyword.replace(" ", "+"))
                try:
                    response = requests.get(formatted_url, timeout=10)
                    soup = BeautifulSoup(response.content, "html.parser")

                    article_list = soup.find("ul", {"data-section": "article_list"})
                    if not article_list:
                        continue

                    articles = article_list.find_all("li")

                    for li in articles:
                        titulo_tag = li.find("h2")
                        titulo = titulo_tag.get_text(strip=True) if titulo_tag else None

                        link_tag = li.find("a", href=True)
                        url_noticia = link_tag["href"] if link_tag else None

                        img_tag = li.find("img")
                        imagem = img_tag["src"] if img_tag else None

                        lide_tag = li.find("p")
                        lide = lide_tag.get_text(strip=True) if lide_tag else None

                        if titulo and url_noticia:
                            relevant_news.append({
                                "titulo": titulo,
                                "url": url_noticia,
                                "imagem": imagem,
                                "lide": lide,
                                "fonte": default_url
                            })

                except Exception as e:
                    print(f"Erro ao acessar {default_url}: {e}")

    return relevant_news


@app.get("/news")
def get_news(keywords: List[str] = Query(DEFAULT_KEYWORDS)):
    """
    Retorna uma lista de notícias encontradas com base nas palavras-chave.
    Você pode passar suas próprias palavras-chave, por exemplo:
    `/news?keywords=frango&keywords=exportação`
    """
    news = search_articles(keywords, WEBSITES)
    return {"total_count": len(news), "data": news}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", "8080")),
    )
