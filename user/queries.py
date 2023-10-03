def query_movie_with_id(id):
    return f'''
    query Movie_with_id {{
        movie_with_id(_id: "{id}") {{
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
    }}'''
