from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'
BOOKING_SERVICE_BASE_URL = "http://172.16.137.68:3201"
MOVIE_SERVICE_BASE_URL = "http://172.16.137.68:3200"

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/bookingsdetails/<userid>", methods=["GET"])
def get_bookings_details(userid):
    r_bookings = requests.get(BOOKING_SERVICE_BASE_URL + '/bookings/' + userid)
    response = []
    # movie_cache = {}
    if r_bookings.status_code == 200:
        for booking in r_bookings.json()['dates']:
            movies_details = []
            for movieid in booking['movies']:
                r_movies = requests.get(MOVIE_SERVICE_BASE_URL + '/movies/' + movieid)
                movies_details.append(r_movies.json())
            response.append({'date': booking['date'], 'movies': movies_details})
    return make_response(jsonify(response), 200)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
