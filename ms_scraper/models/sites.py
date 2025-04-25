# models/sites.py
from sqlalchemy import Column, Integer, String
from models import Base

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True)
    site = Column(String(255), nullable=False)
    url = Column(String(512), nullable=False)
    methode = Column(String(512), nullable=False)