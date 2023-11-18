import json
import uuid
from utilities import MovieRepository, ActorRepository

movie_repository = MovieRepository()
actor_repository = ActorRepository()


def movie_with_id(_, info, _id):
    return movie_repository.get_by_field('id', _id)


def update_movie_rate(_, info, _id, _rating):
    movie_repository.update_rating(_id, _rating)
    return movie_repository.get_by_field('id', _id)


def resolve_actors_in_movie(movie, info):
    actors = []
    for actor in actor_repository.get_all():
        if movie['id'] in actor['films']:
            actors.append(actor)
    return actors


def resolve_films_in_actor(actor, info):
    movies = []
    for movie_id in actor['films']:
        movies.append(movie_repository.get_by_field('id', movie_id))
    return movies


def actor_with_id(_, info, _id):
    return actor_repository.get_by_field('id', _id)


def all_movies(_, info):
    return movie_repository.get_all()


def movie_with_title(_, info, _title):
    return movie_repository.get_by_field('title', _title)


def del_movie_with_id(_, info, _id):
    return movie_repository.delete(_id)


def add_movie(_, info, _movie):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if str(movie["title"]) == str(_movie["title"]):
                return movies['movies']
        movie_uuid = str(uuid.uuid4())
        _movie["id"] = movie_uuid
        movies["movies"].append(_movie)
        with open('{}/data/movies.json'.format("."), "w") as wfile:
            json.dump(movies, wfile)
        return movies['movies']
