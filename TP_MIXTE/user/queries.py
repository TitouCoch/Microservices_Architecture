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