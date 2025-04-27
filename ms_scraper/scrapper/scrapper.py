import time
from db import SessionLocal
from models.sites import Site
import scraping_methods

DELAY_MINUTES = 5

def run_scraper():
    while True:
        print("🔎 Checking sites...")

        db = SessionLocal()
        sites = db.query(Site).all()

        for site in sites:
            method_name = site.methode

            # Vérifie si la méthode existe dans scraping_methods
            if hasattr(scraping_methods, method_name):
                method = getattr(scraping_methods, method_name)
                print(f"Scraping site: {site.site} with method: {method_name}")

                # 🔥 Récupère les articles
                articles = method(site.url)

                if articles:
                    print(f"✅ {len(articles)} articles récupérés pour {site.site}")
                    for article_url in articles:
                        print(f" - {article_url}")
                        # 👉 Ici on pourra ensuite faire insert/check doublons en BDD
                else:
                    print(f"⚠️ Aucun article trouvé pour {site.site}")

            else:
                print(f"⚠️ No scraping method found for: {method_name}")

        db.close()
        print(f"🕒 Sleeping for {DELAY_MINUTES} minutes...")
        time.sleep(DELAY_MINUTES * 60)

if __name__ == "__main__":
    run_scraper()