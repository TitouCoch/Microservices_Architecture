from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
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
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            for date in booking['dates']:
                if str(date['date']) == str(body['date']):
                    if body['movieid'] in date['movies']:
                        return make_response('an existing item already exists', 409)

                    date['movies'].append(body['movieid'])
                    return make_response(jsonify(booking), 200)

            booking['dates'].append({'date': body['date'], 'movies': [body['movieid']]})
            return make_response(jsonify(booking), 200)
    return make_response({"error"}, 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
