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


### Documentation API

Consultez la documentation complète de l'API dans le fichier OpenAPI : [openapi.yaml](./user/openapi.yaml)

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
    "director": "Jane Doe"
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
 "userid": "example_user",
 "dates": [
     {
         "date": "20230101",
         "movies": ["movie1_id", "movie2_id"]
     }
 ]
}
```

### Mettre à jour une réservation

Endpoint: `POST /user/update_booking`

Requête JSON :
```json
{
    "userid": "example_user",
    "dates": [
        {
            "date": "20230102",
            "movies": ["new_movie1_id", "new_movie2_id"]
        }
    ]
}
```



