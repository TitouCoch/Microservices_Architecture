# TP1

## Description

Ce projet implémente une API pour gérer les utilisateurs, les films, les dates et les réservations. Il utilise une architecture de microservices avec Flask et Docker pour fournir un environnement isolé et scalable.

## Configuration Initiale

### Prérequis

- **Python 3.x** : Un langage de programmation interprété, interactif et orienté objet.
- **pip** : Le gestionnaire de paquets pour Python.
- **Docker et Docker Compose** : Pour créer, déployer et gérer des conteneurs d'applications.

### Installation

#### Installer les Dépendances

1. Ouvrez un terminal dans le répertoire racine du projet.
2. Exécutez la commande suivante pour installer toutes les dépendances requises :

   ```bash
   pip install -r requirements.txt
   ```

## Démarrage des Microservices avec Docker

1. Ouvrez un terminal dans le répertoire où se trouve le fichier `docker-compose.yml`.
2. Lancez les microservices en exécutant :

   ```bash
   docker-compose up --build
   ```

   Cette commande va construire et démarrer les conteneurs pour chaque microservice.

## Utilisation

Une fois que les services sont en cours d'exécution, vous pouvez interagir avec eux via leurs endpoints API respectifs.

<a href="https://imgur.com/0T3sQFZ"><img src="https://i.imgur.com/0T3sQFZ.png" title="source: imgur.com" /></a>

## Vous pouvez chercher des films via le endpoint

```python
@app.route("/API/<movie_title>", methods=['GET'])
```

Qui retourne l'image du film si il est trouvé.
