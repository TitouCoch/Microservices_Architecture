def query_movie_with_id(movie_id):
    return f"""
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
    }}"""


def query_movie_name_with_id(movie_id):
    return f"""
    query Movie_with_id {{
        movie_with_id(_id: "{movie_id}") {{
            title
        }}
    }}"""


def query_all_movies():
    return """
    query AllMovies {
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


def mutation_add_movie(movie_input):
    return f"""
    mutation {{
        add_movie(_movie: {{
            title: "{movie_input['title']}",
            director: "{movie_input['director']}",
            rating: {movie_input['rating']}
        }}) {{
            id
            title
            director
            rating
        }}
    }}"""


def mutation_update_movie(movie_id, new_rating):
    return f"""
    mutation {{
        update_movie_rate(_id: "{movie_id}", _rating: {new_rating}) {{
            id
            title
            rating
        }}
    }}"""


def mutation_delete_movie(movie_id):
    return f"""
    mutation {{
        del_movie_with_id(_id: "{movie_id}") {{
            id
        }}
    }}"""


def query_movie_with_title(title):
    return f"""
    query {{
        movie_with_title(_title: "{title}") {{
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
    }}"""
