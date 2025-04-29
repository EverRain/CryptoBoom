import re
from transformers import pipeline
from typing import Optional

# Liste simplifiée des marchés financiers possibles (à étendre)
MARCHES = {
    "bitcoin": ["bitcoin", "btc"],
    "ethereum": ["ethereum", "eth"],
    "tesla": ["tesla", "elon musk"],
    "mastercard": ["mastercard"],
    "metamask": ["metamask"],
    "coinbase": ["coinbase"],
    "dogecoin": ["dogecoin", "doge"],
}

# Modèle francophone de sentiment (camembert fine-tuné)
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def detecter_marche(content: str) -> Optional[str]:
    content_lower = content.lower()
    for marche, keywords in MARCHES.items():
        if any(k in content_lower for k in keywords):
            return marche
    return None

def analyser_tendance(content: str):
    result = sentiment_pipeline(content[:512])[0]
    label = result["label"]

    # On convertit les étoiles en tendance
    stars = int(label[0])  # ex: "4 stars" → 4
    if stars <= 2:
        return 1  # négatif
    elif stars == 3:
        return 0  # neutre
    else:
        return 2  # positif