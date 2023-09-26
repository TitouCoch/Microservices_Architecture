from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
    schedule = json.load(jsf)["schedule"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"


@app.route("/showtimes", methods=["GET"])
def get_times():
    return make_response(jsonify(schedule), 200)


@app.route("/showmovies/<date>", methods=["GET"])
def get_movies_by_date(date):
    for d in schedule:
        if str(d['date']) == str(date):
            return make_response(jsonify(d), 200)
    return make_response({"error": "No date found"})


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
