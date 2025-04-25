# CryptoBoom


# Commande pour migration db

poetry run alembic revision --autogenerate -m "nom de la migration"
poetry run alembic upgrade head