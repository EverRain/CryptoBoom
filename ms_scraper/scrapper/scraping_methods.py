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

# url = "https://journalducoin.com/"
# articles = scraper_lejournalducoin(url)
# for article in articles:
#     print(article)
