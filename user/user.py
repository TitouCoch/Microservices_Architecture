from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'
BOOKING_SERVICE_BASE_URL = "http://172.16.137.68:3201"
MOVIE_GRAPHQL_SERVICE_BASE_URL = "http://172.16.137.68:3001/graphql"

with open('{}/data/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


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

@app.route("/bookingsdetails/<userid>", methods=["GET"])
def get_bookings_details(userid):
    r_bookings = requests.get(BOOKING_SERVICE_BASE_URL + '/bookings/' + userid)
    print(r_bookings.json())
    response = []
    # movie_cache = {}
    if r_bookings.status_code == 200:
        for booking in r_bookings.json()['dates']:
            movies_details = []
            for movieid in booking['movies']:
                r_movies = requests.post(MOVIE_GRAPHQL_SERVICE_BASE_URL,
                                         json={'query': query_movie_with_id(movieid)})
                movies_details.append(r_movies.json()['data']['movie_with_id'])
            response.append({'date': booking['date'], 'movies': movies_details})
    return make_response(jsonify(response), 200)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
