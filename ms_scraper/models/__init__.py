# models/__init__.py
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .articles import Article
from .sites import Site
from .analyse_article import ArticleAnalyse