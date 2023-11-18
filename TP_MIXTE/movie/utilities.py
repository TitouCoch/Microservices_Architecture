import json


class MovieRepository:
    movies: list = []

    def __init__(self):
        with open('{}/data/movies.json'.format("."), "r") as file:
            data = json.load(file)
            self.movies = data['movies']

    def get_all(self):
        return self.movies

    def get_by_field(self, field, value):
        for movie in self.movies:
            if movie[field] == value:
                return movie
        raise Exception("Movie not found")

    def add(self, movie):
        self.movies.append(movie)
        self.save()
        return movie

    def delete(self, id):
        self.movies = [movie for movie in self.movies if movie['id'] != id]
        self.save()

    def update_rating(self, id, rating):
        for movie in self.movies:
            if movie['id'] == id:
                movie['rating'] = rating
                print(movie, rating)
        self.save()

    def save(self):
        with open('{}/data/movies.json'.format("."), "w") as wfile:
            json.dump({"movies": self.movies}, wfile)


class ActorRepository:

    def __init__(self):
        with open('{}/data/actors.json'.format("."), "r") as file:
            data = json.load(file)
            self.actors = data['actors']

    def get_all(self):
        return self.actors

    def get_by_field(self, field, value):
        for actor in self.actors:
            if actor[field] == value:
                return actor
        return None

    def add(self, actor):
        self.actors.append(actor)
        self.save()
        return actor

    def save(self):
        with open('{}/data/actors.json'.format("."), "w") as wfile:
            json.dump({"actors": self.actors}, wfile)

    def exist(self, actor):
        for a in self.actors:
            if ((hasattr(actor, 'id') and a['id'] == actor.id)
                    or (hasattr(actor, 'firstname') and a['firstname'] == actor.firstname
                        and hasattr(actor, 'lastname') and a['lastname'] == actor.lastname)):
                return True
        return False

    def add_movie(self, actor_id, movie_id):
        for actor in self.actors:
            if actor['id'] == actor_id:
                actor['films'].append(movie_id)
        self.save()
