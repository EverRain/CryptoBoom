from sqlalchemy import Column, Integer, String, ForeignKey
from models import Base

class ArticleAnalyse(Base):
    __tablename__ = "articles_analyses"

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    market_place = Column(String(255), nullable=False)  # e.g. "Bitcoin", "Tesla"
    tendance = Column(Integer, nullable=False)  # 0 = neutre, 1 = négatif, 2 = positif