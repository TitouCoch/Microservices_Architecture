from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'
booking_service_url = "http://172.20.10.2:3201/"
movies_service_url = "http://172.20.10.2:3200/"

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/users", methods=['GET'])
def get_json():
    res = make_response(jsonify(users), 200)
    return res


@app.route("/users/<userid>", methods=['GET'])
def get_info_movies_user(userid):
    # Obtenez les données de réservation
    booking_response = requests.get(f"{booking_service_url}/bookings/{userid}")
    if booking_response.status_code != 200:
        return make_response(jsonify({"error": "Booking data not found"}), 404)

    booking = booking_response.json()

    # Obtenez les données des films
    movies_response = requests.get(f"{movies_service_url}/json")
    if movies_response.status_code != 200:
        return make_response(jsonify({"error": "Movie data not found"}), 404)

    movies = movies_response.json()

    # Créez une liste de films correspondants
    result = []

    for data in booking["dates"]:
        for booking_movie in data["movies"]:
            for movie in movies:
                if movie["id"] == booking_movie:
                    result.append(movie)

    res = make_response(jsonify(result), 200)
    return res


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
