from bs4 import BeautifulSoup
import requests
from sqlalchemy.orm import Session
from models.articles import Article
from models.analyse_article import ArticleAnalyse
from db import SessionLocal
import datetime
from analyses import detecter_marche, analyser_tendance

def scraper_contenu_article(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur HTTP {response.status_code} pour {url}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # ➤ Titre
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Sans titre"

    # ➤ Contenu principal
    article_block = soup.select_one("div.article.sidebar-right div.content")
    if not article_block:
        print("❌ Contenu non trouvé pour", url)
        return None

    # ➤ On extrait paragraphes + titres
    texte_article = ""
    for elem in article_block.find_all(['p', 'h2', 'h3', 'ul', 'li']):
        texte_article += elem.get_text(separator=" ", strip=True) + "\n\n"

    return {
        'title': title,
        'content': texte_article.strip()
    }

def scraper_lejournalducoin(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur HTTP {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', class_='title'):
        href = a_tag.get('href')
        if href and href.startswith("https://journalducoin.com/"):
            links.append(href)

    # Maintenant on traite chaque article
    session: Session = SessionLocal()
    nouvelles_urls = []

    for link in links:
        # Doublon ?
        exists = session.query(Article).filter(Article.url == link).first()
        if exists:
            continue

        # Scraping contenu
        data = scraper_contenu_article(link)
        if not data:
            continue

        # Création et insertion
        nouvel_article = Article(
            title=data['title'],
            url=link,
            content=data['content'],
            source="JournalDuCoin",
            scraped_at=datetime.datetime.utcnow()
        )

        session.add(nouvel_article)
        session.commit()

        nouvelles_urls.append(link)
        # Analyse
        market = detecter_marche(data['content'])
        if market:
            tendance = analyser_tendance(data['content'])
            analyse = ArticleAnalyse(
                article_id=nouvel_article.id,
                market_place=market,
                tendance=tendance
            )
            session.add(analyse)
            session.commit()
            print(f"🔎 Analyse : marché={market}, tendance={tendance}")
        else:
            print("⚠️ Aucun marché détecté, analyse non enregistrée.")
        print(f"✅ Article ajouté : {data['title']}")

    session.close()
    return nouvelles_urls
