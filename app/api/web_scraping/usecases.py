import requests
from bs4 import BeautifulSoup

keywords = [
    "indústria avícola", "processamento de frango", "frigorífico", "exportação de frango",
    "importação de frango", "mercado avícola", "preço do frango", "custos industriais",
    "cadeia produtiva", "produção intensiva", "automação industrial", "logística avícola",
    "qualidade da carne", "normas sanitárias", "inspeção federal", "certificação de alimentos",
    "SIF", "selo SIF", "vistorias SIF", "inovação tecnológica", "biotecnologia avícola",
    "indústria de alimentos", "produção industrial", "processamento de carne", "abate industrial",
    "estocagem frigorífica", "distribuição de frango", "armazenamento a frio", "exportação de ovos",
    "indústria de ovos", "embalagem de frango", "rotulagem de alimentos", "industria alimentícia",
    "produção em larga escala", "controle de qualidade", "mercado internacional", "exportadores de frango",
    "investimentos industriais", "sustentabilidade industrial", "impacto ambiental", "normas ISO",
    "gestão de produção", "automatização de linha de produção", "processamento de cortes",
    "industrialização do frango", "cadeia logística", "indústria de proteína animal",
    "produção de alimentos processados", "tecnologia de abate", "engenharia de alimentos",
    "segurança alimentar", "regulamentação avícola", "granjas comerciais", "produção de pintinhos",
    "alimentação de frangos", "sanidade avícola"
]

websites = [{"https://www.cnnbrasil.com.br": "https://www.cnnbrasil.com.br/?search={search}&orderby=date&order=desc"}]

def search_articles(keywords: list[str], websites: list[dict[str, str]]):
        
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
                            print("Nenhuma lista de artigos encontrada.")
                            exit()

                        # pega todos os <li> dentro da lista
                        articles = article_list.find_all("li")

                        noticias = []

                        for li in articles:
                            # título
                            titulo_tag = li.find("h2")
                            titulo = titulo_tag.get_text(strip=True) if titulo_tag else None

                            # URL da notícia
                            link_tag = li.find("a", href=True)
                            url_noticia = link_tag["href"] if link_tag else None

                            # imagem
                            img_tag = li.find("img")
                            imagem = img_tag["src"] if img_tag else None

                            # lide (resumo) — pode não existir, então testamos se há um <p> ou outro texto
                            lide_tag = li.find("p")
                            lide = lide_tag.get_text(strip=True) if lide_tag else None

                            # monta o dicionário
                            if titulo and url_noticia:
                                noticias.append({
                                    "titulo": titulo,
                                    "url": url_noticia,
                                    "imagem": imagem,
                                    "lide": lide
                                })

                        # exibe
                        for n in noticias:
                            print(n)
                        # for h3 in headline_tags:
                        #     headline = h3.get_text(strip=True)
                        #     parent_a = h3.find_parent("a")
                        #     link = parent_a.get("href") if parent_a else None
                        #     relevant_news.append({'headline': headline, 'link':link, 'image':img,})

                    except Exception as e:
                        print(f"Erro ao acessar {default_url}: {e}")
    
        return relevant_news

search_articles(keywords, websites)
