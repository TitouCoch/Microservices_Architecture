from flask import Flask, request, jsonify, make_response
import requests
import json
app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'
showtime_service_url = "http://172.20.10.2:3202/"

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]


@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


@app.route("/bookings", methods=['GET'])
def get_json():
    res = make_response(jsonify(bookings), 200)
    return res


@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            res = booking
            return res
    return make_response(jsonify({"error": "Movie ID not found"}), 400)


@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
    # Recuperer les données JSON de la requête
    body = request.get_json()
    date = body["dates"][0]["date"]
    movie = body["dates"][0]["movies"]

    # Vérifier si la date existe dans le service Showtime
    showtime_response = requests.get(f"{showtime_service_url}/showmovies/{date}")
    if showtime_response.status_code != 200:
        return make_response(jsonify({"error": "Date doesn't exist in showtime"}), 409)

    showtime = showtime_response.json()
    movie_found = False

    # Vérifier si le film existe dans les données Showtime
    for showtime_movie in showtime["movies"]:
        if str(showtime_movie) == movie[0]:
            movie_found = True
            break

    if not movie_found:
        return make_response(jsonify({"error": "Movie doesn't exist in showtime"}), 400)

    # Vérifier si l'utilisateur a déjà des réservations
    for booking in bookings:
        if booking["userid"] == userid:
            for param_booking in booking["dates"]:
                # Vérifier si la date de réservation existe
                if param_booking["date"] == date:
                    # Vérifier si le film est déjà réservé pour cette date
                    if movie[0] in param_booking['movies']:
                        return make_response(jsonify({"error": "an existing item already exists"}), 400)
                    # Ajouter le film à la date de réservation existante
                    param_booking["movies"].append(movie[0])
                    return make_response(jsonify({"message": "Booking created"}), 200)
            # Si la date de réservation n'existe pas, ajouter une nouvelle date de réservation
            booking["dates"].append({"date": date, "movies": movie})
            return make_response(jsonify({"message": "Booking created"}), 200)

    # Si l'utilisateur n'a pas de réservations existantes, ajouter une nouvelle réservation
    bookings.append(body)
    return make_response(jsonify({"message": "Booking created"}), 200)

if __name__ == "__main__":
   print("Server running in port %s" % PORT)
   app.run(host=HOST, port=PORT)
