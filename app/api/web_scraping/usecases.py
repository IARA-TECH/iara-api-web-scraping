from typing import List
import requests
from bs4 import BeautifulSoup
from ...shared.exceptions.internal_server_error import InternalServerError
from .models import getData


def get(keywords: List[str] = None, websites: List[dict[str, str]] = None) -> List[getData]:

    if not keywords:
        keywords = [
        'inovação-industrial', 'agropecuária', 'producao-frango'
        ]

    if not websites: 
        websites = [{
            "https://www.cnnbrasil.com.br": 
            "https://www.cnnbrasil.com.br/?search={search}&orderby=date&order=desc",
        }]

    relevant_news = []

    for website in websites:
        for default_url, search_url in website.items():
            for keyword in keywords:
                formatted_url = search_url.format(search=keyword.replace(" ", "+"))
                print(formatted_url)
                try:
                    response = requests.get(formatted_url, timeout=10)
                    soup = BeautifulSoup(response.content, "html.parser")

                    article_list = soup.find("ul", {"data-section": "article_list"})
                    if not article_list:
                        continue

                    articles = article_list.find_all("li")

                    count = 0
                    for li in articles:

                        if count == 6:
                            break

                        titulo_tag = li.find("h2")
                        titulo = titulo_tag.get_text(strip=True) if titulo_tag else None

                        link_tag = li.find("a", href=True)
                        url_noticia = link_tag["href"] if link_tag else None

                        img_tag = li.find("img")
                        imagem = img_tag["src"] if img_tag else None

                        lide_tag = li.find("p")
                        lide = lide_tag.get_text(strip=True) if lide_tag else None

                        if titulo and url_noticia:
                            if not any(n["titulo"] == titulo or n["url"] == url_noticia for n in relevant_news):
                                relevant_news.append({
                                    "titulo": titulo,
                                    "url": url_noticia,
                                    "imagem": imagem,
                                    "lide": lide,
                                    "fonte": default_url
                                })
                                count = count + 1

                except Exception as e:
                    raise InternalServerError('Buscar notícias')

    return relevant_news