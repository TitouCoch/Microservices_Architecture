def query_movie_with_id(movie_id):
    return """
    query Movie_with_id {{
        movie_with_id(_id: "{movie_id}") {{
            id
            title
            director
            rating
            actors {{
                id
                firstname
                lastname
                birthyear
            }}
        }}
    }}""".format(movie_id=movie_id)


def query_movie_with_title(movie_title):
    return """
    query Movie_with_title {{
        movie_with_title(title: "{movie_title}") {{
            id
            title
            director
            rating
            actors {{
                id
                firstname
                lastname
                birthyear
            }}
        }}
    }}""".format(movie_title=movie_title)


def query_all_movies():
    return """
    query All_movies {
        all_movies {
            id
            title
            director
            rating
            actors {
                id
                firstname
                lastname
                birthyear
            }
        }
    }"""


def query_actor_with_id(actor_id):
    return """
    query actor_with_id {{
        actor_with_id(_id: "{actor_id}") {{
            id
            firstname
            lastname
            birthyear
            films {{
                id
                title
                director
                rating
            }}
        }}
    }}""".format(actor_id=actor_id)


def mutation_update_movie_rate(movie_id, rating):
    return """    
    mutation Update_movie_rate {{
        update_movie_rate(_id: "{movie_id}", _rating: {rating} ) {{
            id
            title
            director
            rating
            actors {{
                id
                firstname
                lastname
                birthyear
            }}
        }}
    }}""".format(movie_id=movie_id, rating=rating)


def mutation_del_movie_with_id(movie_id):
    return """mutation Del_movie_with_id {{
        del_movie_with_id(_id: "{movie_id}") {{
            id
            title
            director
            rating
            actors {{
                id
                firstname
                lastname
                birthyear
            }}
        }}
    }}""".format(movie_id=movie_id)


def mutation_add_movie(title, director, rating):
    return """
    mutation Add_movie {{
        add_movie(title: "{title}", director: "{director}", rating: {rating}) {{
            id
            title
            director
            rating
            actors {{
                id
                firstname
                lastname
                birthyear
            }}
        }}
    }}""".format(title=title, director=director, rating=rating)
