from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/data/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


@app.route("/bookings", methods=['GET'])
def get_bookings():
    return make_response(jsonify(bookings), 200)


@app.route("/bookings/<userid>", methods=["GET"])
def get_bookings_from_user(userid):
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            return make_response(booking, 200)
    return make_response({"error": "bad input parameter"}, 400)


@app.route("/bookings/<userid>", methods=["POST"])
def add_booking_user(userid):
    body = request.get_json()
    date, movie_id = body['date'], body['movieid']
    r = requests.get('http://172.16.137.68:3202/showmovies/' + body['date'])
    res_body = r.json()
    if not movie_id in res_body['movies']:
        return make_response({'error': 'movie is not available for booking'}, 400)
    user_booking = next((x for x in bookings if x['userid'] == userid), None)
    if user_booking is None:
        bookings.append({'userid': userid, 'bookings': [{'movieid': movie_id, 'date': date}]})
    else:
        booking_date = next(x for x in user_booking['dates'] if x['date'] == date)
        print(booking_date)
        if movie_id in booking_date['movies']:
            return make_response({'error': 'movie already booked for this user'}, 400)
        else:
            booking_date['movies'].append(movie_id)
    return make_response(user_booking, 200)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
