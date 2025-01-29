# Étape 1 : Utiliser l'image officielle de Python comme image de base

FROM python:3.11-slim

# Étape 2 :  répertoire de travail à l'intérieur du conteneur

WORKDIR /app

# Étape 3 : Copier le fichier requirements.txt dans le conteneur

COPY requirements.txt /app/

# Étape 4  Installer les dépendances Python dans le conteneur

RUN pip install --no-cache-dir -r requirements.txt

# Étape 5  Copier l'ensemble des fichiers du projet dans le conteneur
COPY . /app/

# Étape 6 : Exposer le port sur lequel FastAPI va écouter
EXPOSE 8002

# Étape 7 : Définir la commande pour démarrer l'application FastAPI avec uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]

