import json
import uuid


def movie_with_id(_, info, _id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie


def update_movie_rate(_, info, _id, _rating):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rating
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    print(newmovie)
    return newmovie


def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data['actors'] if movie['id'] in actor['films']]
        return actors


def resolve_films_in_actor(actor, info):
    with open('{}/data/movies.json'.format("."), "r") as file:
        data = json.load(file)
        movies = [movie for movie in data['movies'] if movie['id'] in actor['films']]
        return movies


def actor_with_id(_, info, _id):
    with open('{}/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        for actor in data['actors']:
            if actor['id'] == _id:
                return actor


def all_movies(_, info):
    with open('{}/data/movies.json'.format("."), "r") as file:
        data = json.load(file)
        print(data)
        return data['movies']


def movie_with_title(_, info, _title):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)['movies']
        for movie in movies:
            if str(movie['title']) == str(_title):
                return movie


def delete_a_movie(_, info, _id):
    print('[MOVIE] Deleting movie with id {}'.format(_id))
    new_movies = {"movies": []}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)['movies']
        for movie in movies:
            if str(movie['id']) == str(_id):
                movieToDel = movie
        if not movieToDel:
            return False
        movies.remove(movieToDel)
        new_movies['movies'] = movies

    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(new_movies, wfile)
        return True


def add_a_movie(_, info, _movie):
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)

    movie = {
        'title': _movie['title'],
        'rating': _movie['rating'],
        'director': _movie['director'],
        'id': str(uuid.uuid4())
    }
    movies['movies'].append(movie)
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(movies, wfile)
    return movie

# TODO
