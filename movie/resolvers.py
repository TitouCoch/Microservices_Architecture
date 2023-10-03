import uuid

from utilities import MovieRepository, ActorRepository

actor_repository = ActorRepository()
movie_repository = MovieRepository()


def resolve_actors_in_movie(movie, info):
    return [actor for actor in actor_repository.get_all() if movie['id'] in actor['films']]


def resolve_films_in_actor(actor, info):
    return [movie for movie in movie_repository.get_all() if movie['id'] in actor['films']]


def movie_with_id(_, info, _id):
    return movie_repository.get_by_field('id', _id)


def update_movie_rate(_, info, _id, _rating):
    movie_repository.update_rating(_id, _rating)
    return movie_repository.get_by_field('id', _id)


def actor_with_id(_, info, _id):
    return actor_repository.get_by_field('id', _id)


def all_movies(_, info):
    return movie_repository.get_all()


def movie_with_title(_, info, _title):
    return movie_repository.get_by_field('title', _title)


def delete_a_movie(_, info, _id):
    if movie_repository.get_by_field('id', _id) is None:
        return False
    movie_repository.delete(_id)
    return True


def add_a_movie(_, info, _movie):
    new_movie = movie_repository.add({
        "id": str(uuid.uuid4()),
        "title": _movie['title'],
        "director": _movie['director'],
        "rating": _movie['rating']
    })
    if _movie['actors'] is not None:
        for actor in _movie['actors']:
            print(actor)
            res = actor_repository.exist(actor)
            if res is False:
                actor_repository.add({
                    "id": str(uuid.uuid4()),
                    "firstname": actor['firstname'],
                    "lastname": actor['lastname'],
                    "birthyear": actor['birthyear'],
                    "films": [new_movie['id']]
                })
            else:
                actor_repository.add_movie(res['id'], new_movie['id'])

    return new_movie
