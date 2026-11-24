# 1. Image de base
FROM python:3.12-slim

# 2. Répertoire de travail dans le conteneur
WORKDIR /code

# 3. Copier requirements.txt d'abord, puis installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copier le code de l'application
COPY app/ app/
COPY run.py .

# 5. Dossier pour la base de données (volume en Mission 4)
RUN mkdir /data
ENV DATABASE_PATH=/data/incidents.db

# 6. Port de l'application
EXPOSE 5000

# 7. Commande de démarrage
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
