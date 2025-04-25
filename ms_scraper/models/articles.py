from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
import datetime

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    url = Column(String(512), nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String(255), nullable=False)
    scraped_at = Column(DateTime, default=datetime.datetime.utcnow)