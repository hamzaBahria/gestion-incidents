# Gestion des incidents informatiques

Application web de gestion des incidents informatiques signalés par les étudiants
et les enseignants. Projet DevOps : développement, conteneurisation et déploiement
automatisé avec Docker et GitHub Actions.

## Fonctionnalités

- Ajouter un incident
- Afficher la liste des incidents (avec filtre par statut)
- Consulter les détails d'un incident
- Modifier le statut (nouveau, en cours, résolu)
- Supprimer un incident

Un incident contient : identifiant, titre, description, lieu, priorité
(faible, moyenne, élevée) et statut.

## Technologies

Python 3.12, Flask, SQLite, Gunicorn, pytest, Docker, Docker Compose,
GitHub Actions, GitHub Container Registry (GHCR).

## Structure du dépôt

```
gestion-incidents/
├── app/                  # Application Flask (routes, base, templates)
├── tests/                # Tests automatisés pytest
├── Dockerfile
├── compose.yaml          # Démarrage avec construction locale
├── compose.deploy.yaml   # Déploiement à partir de l'image GHCR
├── requirements.txt
├── pytest.ini
└── .github/workflows/
    ├── ci.yml            # Intégration continue
    └── cd.yml            # Publication dans GHCR
```

## Installation en local

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Application disponible sur http://localhost:5000

## Lancer les tests

```bash
pytest -v
```

## Docker

```bash
docker build -t gestion-incidents:latest .
docker run -d --name incidents -p 5000:5000 gestion-incidents:latest
docker ps
docker logs incidents
```

## Docker Compose (développement)

```bash
docker compose up -d --build   # démarrer
docker compose ps              # vérifier
docker compose logs            # journaux
docker compose down            # arrêter
```

Les données SQLite sont conservées dans le volume `incidents-data`
(montée sur `/data`). Ne pas utiliser `docker compose down -v`
sauf pour supprimer les données.

## Pipeline CI/CD

### CI (`ci.yml`)
Déclenché sur **push** et **pull request** vers `main` :
1. Récupération du code
2. Installation de Python et des dépendances
3. Exécution des tests pytest
4. Validation de `compose.yaml` et `compose.deploy.yaml`
5. Construction de l'image Docker

### CD (`cd.yml`)
Déclenché sur **push** vers `main` :
1. Job `test` : exécution des tests
2. Job `build-and-push` (dépend de `test`) : connexion à GHCR avec
   `GITHUB_TOKEN`, construction et publication de l'image avec deux tags :
   - `latest`
   - le SHA du commit (`github.sha`)

La publication n'a lieu que si les tests réussissent.

## Build, publication, déploiement

| Étape | Rôle | Où |
|---|---|---|
| Build | Construire l'image à partir du Dockerfile | GitHub Actions |
| Publication | Envoyer l'image dans le registre GHCR | GitHub Actions → GHCR |
| Déploiement | Récupérer l'image et la démarrer | Machine de déploiement |

## Déploiement

L'image publiée est : `ghcr.io/hamzabahria/gestion-incidents`

```bash
docker compose -f compose.deploy.yaml pull
docker compose -f compose.deploy.yaml up -d
docker compose -f compose.deploy.yaml ps
docker compose -f compose.deploy.yaml logs
```

Si le package est privé, s'authentifier d'abord :

```bash
echo "TOKEN" | docker login ghcr.io -u NOM_UTILISATEUR --password-stdin
```

(Le token ne doit jamais être partagé ni écrit dans le dépôt.)

## Mettre à jour l'application

1. Modifier le code, puis `git commit` et `git push origin main`
2. Vérifier que les pipelines CI et CD réussissent
3. Sur la machine de déploiement :

```bash
docker compose -f compose.deploy.yaml pull
docker compose -f compose.deploy.yaml up -d
```

## Auteurs

- Hamza Bahria
- Koussay Benna
