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
        db.close()

        for site in sites:
            method_name = site.methode

            # Vérifie si la méthode existe dans scraping_methods
            if hasattr(scraping_methods, method_name):
                method = getattr(scraping_methods, method_name)
                print(f"Scraping site: {site.site} with method: {method_name}")
                method(site.url)
            else:
                print(f"⚠️ No scraping method found for: {method_name}")

        print(f"🕒 Sleeping for {DELAY_MINUTES} minutes...")
        time.sleep(DELAY_MINUTES * 60)

if __name__ == "__main__":
    run_scraper()