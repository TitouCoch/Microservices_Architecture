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

Les endpoints sont accéssible depuis les URL suivantes : 

```json
http://localhost:3203/users
https://localhost:3200/movies
http://localhost:3201/bookings
http://localhost:3202/showtimes
```

Une fois que les services sont en cours d'exécution, vous pouvez interagir avec eux via leurs endpoints API respectifs.

<a href="https://imgur.com/0T3sQFZ"><img src="https://i.imgur.com/0T3sQFZ.png" title="source: imgur.com" /></a>

## TP ROUGE - Vous pouvez chercher des films via le endpoint

```python
url_api_movies = "https://www.omdbapi.com/"
apikey = "5133f7b6"

@app.route("/API/<movie_title>", methods=['GET'])
def get_movie_bytitle_from_api(movie_title):
    info_movie = requests.get(f"{url_api_movies}?apikey={apikey}&s={movie_title}")
    if info_movie.status_code != 200:
        return make_response(jsonify({"error": "No movie Found"}), 404)
    info_movie = info_movie.json()
    return make_response(f"<img src='{info_movie['Search'][0]['Poster']}'>", 200)

```

Qui retourne l'image du film si il est trouvé.
