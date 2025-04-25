from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
import datetime

Base = declarative_base()

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True)
    site = Column(String(255), nullable=False)
    url = Column(String(512), nullable=False)
    methode = Column(String(512), nullable=False)