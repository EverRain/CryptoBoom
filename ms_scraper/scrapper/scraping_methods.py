from bs4 import BeautifulSoup
import requests

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

    for link in links:
        print(link)
    return links

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
