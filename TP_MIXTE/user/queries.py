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
