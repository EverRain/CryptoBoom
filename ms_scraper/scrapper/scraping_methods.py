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
        # # Analyse
        # market = detecter_marche(data['content'])
        # if market:
        #     tendance = analyser_tendance(data['content'])
        #     analyse = ArticleAnalyse(
        #         article_id=nouvel_article.id,
        #         market_place=market,
        #         tendance=tendance
        #     )
        #     session.add(analyse)
        #     session.commit()
        #     print(f"🔎 Analyse : marché={market}, tendance={tendance}")
        # else:
        #     print("⚠️ Aucun marché détecté, analyse non enregistrée.")
        # print(f"✅ Article ajouté : {data['title']}")

    session.close()
    return nouvelles_urls


def scraper_cointelegraph(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur HTTP {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', class_='post-card-inline__title-link'):
        href = a_tag.get('href')
        if href and href.startswith("https://cointelegraph.com"):
            links.append(href)

    return list(set(links))

def scraper_cryptoast(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur HTTP {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', class_='post-title'):
        href = a_tag.get('href')
        if href and href.startswith("https://cryptoast.fr"):
            links.append(href)

    return list(set(links))

def scraper_decrypt(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur HTTP {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', class_='article-card-title-link'):
        href = a_tag.get('href')
        if href and href.startswith("https://decrypt.co"):
            links.append(href)

    return list(set(links))

def scraper_blockworks(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur HTTP {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith("/news/"):
            full_url = "https://blockworks.co" + href
            links.append(full_url)

    return list(set(links))


# url = "https://journalducoin.com/"
# articles = scraper_lejournalducoin(url)
# for article in articles:
#     print(article)
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
def scraper_bloomberg(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/news/articles/'):
            full_url = 'https://www.bloomberg.com' + href
            links.append(full_url)

    return list(set(links))

def scraper_reuters(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/article/') or href.startswith('/business/'):
            full_url = 'https://www.reuters.com' + href
            links.append(full_url)

    return list(set(links))

def scraper_cnbc(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/202') and 'cnbc.com' not in href:
            full_url = 'https://www.cnbc.com' + href
            links.append(full_url)

    return list(set(links))

def scraper_financial_times(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/content/'):
            full_url = 'https://www.ft.com' + href
            links.append(full_url)

    return list(set(links))

def scraper_wsj(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/articles/'):
            full_url = 'https://www.wsj.com' + href
            links.append(full_url)

    return list(set(links))

def scraper_investopedia(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/terms/') or href.startswith('/articles/'):
            full_url = 'https://www.investopedia.com' + href
            links.append(full_url)

    return list(set(links))

def scraper_marketwatch(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/story/'):
            full_url = 'https://www.marketwatch.com' + href
            links.append(full_url)

    return list(set(links))

def scraper_seekingalpha(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/article/'):
            full_url = 'https://seekingalpha.com' + href
            links.append(full_url)

    return list(set(links))

def scraper_yahoo_finance(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if '/news/' in href:
            if href.startswith('http'):
                links.append(href)
            else:
                full_url = 'https://finance.yahoo.com' + href
                links.append(full_url)

    return list(set(links))

def scraper_the_economist(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/'):
            full_url = 'https://www.economist.com' + href
            links.append(full_url)

    return list(set(links))

def scraper_forbes(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/sites/') or href.startswith('/profile/'):
            full_url = 'https://www.forbes.com' + href
            links.append(full_url)

    return list(set(links))

def scraper_bfm_crypto(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/crypto/') and 'video' not in href:
            full_url = 'https://www.bfmtv.com' + href
            links.append(full_url)

    return list(set(links))

def scraper_boursorama_finances(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/bourse/actualites/') and 'finances' in href:
            full_url = 'https://www.boursorama.com' + href
            links.append(full_url)

    return list(set(links))

def scraper_lesechos_finance(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/finance-marches/') or href.startswith('/marches/'):
            full_url = 'https://www.lesechos.fr' + href
            links.append(full_url)

    return list(set(links))

def scraper_tradingview_news(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/news/') and 'markets' in href:
            full_url = 'https://fr.tradingview.com' + href
            links.append(full_url)

    return list(set(links))

def scraper_investing_news(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/news/') and 'headlines' not in href:
            full_url = 'https://fr.investing.com' + href
            links.append(full_url)

    return list(set(links))

def scraper_agefi_grand_angle(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/news/') or href.startswith('/investisseurs-institutionnels/actualites/'):
            full_url = 'https://www.agefi.fr' + href
            links.append(full_url)

    return list(set(links))

def scraper_finary_actualites(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur : {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/fr/actualites-produit/'):
            full_url = 'https://finary.com' + href
            links.append(full_url)

    return list(set(links))
