# TP MIXTE 

## Movie and User Service API

## Description

Ce projet implémente une API pour gérer les utilisateurs, les films, les dates et les réservations.

## Configuration initiale

### Prérequis

- Python 3.x
- pip (Gestionnaire de paquets Python)

### Installation

1. **Configurer l'interpréteur Python**  
   Assurez-vous que Python 3.x est installé sur votre système. Vous pouvez le vérifier en exécutant `python --version` dans votre terminal.

2. **Installer les dépendances**  
   Installez toutes les dépendances requises en exécutant la commande suivante :

```shell
pip install -r requirements.txt
```

3. **Lancement des microservices avec Docker**
   Utilisez Docker Compose pour construire et démarrer les microservices. Exécutez la commande suivante :

```shell
docker-compose up --build
```

### Documentation API

Consultez la documentation complète de l'API dans le fichier OpenAPI : [openapi.yaml](./user/tp-mixte-rest-endpoints.yaml), ouvrir dans [Swagger Editor](https://editor.swagger.io/).

## Test des Endpoints avec Postman

Pour tester les endpoints qui nécessitent un body query, voici quelques exemples de requêtes JSON que vous pouvez utiliser dans Postman.


### Ajouter un utilisateur
Endpoint: ```POST /user/add_user/{userid}```

Requête JSON :
```json
{
    "id": "new_user",
    "name": "John Doe",
    "email": "john.doe@example.com"
}
```

### Ajouter un film
Endpoint: ```POST /user/add_movie```

Requête JSON :

```json
{
    "title": "New Movie",
    "genre": "Action",
    "director": "Jane Doe",
    "rating": 9.0
}
```

### Mettre à jour un film
Endpoint: ```POST /user/update_movie/{movieid}```

Requête JSON :

```json
{
    "rating": "8.5"
}
```

### Ajouter une réservation

Endpoint: `POST /user/add_booking`

Requête JSON :
```json
{
   "movieId": "example_user",
   "date": "23082023"
}
```

### Ajouter un Showtime

Endpoint: `POST /user/add_showtime`

Requête JSON :
```json
{
    "date": "20230101",
    "movie_ids": [
        "96798c08-d19b-4986-a05d-7da856efb697",
        "4b96fd92-dec7-4bc4-b6f0-e60055f5c840"
    ]
}
```


### Modifier un Showtime

Endpoint: `POST /user/update_showtime`

Requête JSON :
```json
{
    "date": "20230101",
    "movie_ids": [
        "b18abb8f-5ac2-494d-9c86-57029e46ca59"
    ]
}
```


