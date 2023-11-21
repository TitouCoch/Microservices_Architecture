from flask import Flask, jsonify, make_response
import requests
import json


app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'
booking_service_url = "http://localhost:3201/"
movies_service_url = "http://localhost:3200/"


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


@app.route("/users/<userid>/<date>", methods=['GET'])
def get_movies_for_user_and_date(userid, date):
    booking_response = requests.get(f"{booking_service_url}/bookings/{userid}")

    # Vérifiez si la réponse du service de réservation a retourné avec succès
    if booking_response.status_code != 200:
        return make_response(jsonify({"error": "Booking data not found"}), 404)

    booking = booking_response.json()

    result = []

    for data in booking["dates"]:
        if data["date"] == date:
            for booking_movie in data["movies"]:
                result.append(booking_movie)

    if not result:
        return make_response(jsonify({"error": "No reservation for this day"}), 404)

    res = make_response(jsonify(result), 200)
    return res


if __name__ == "__main__":
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)
