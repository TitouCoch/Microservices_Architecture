from flask import Flask, jsonify, make_response
import requests
import json
import grpc
import booking_pb2
import booking_pb2_grpc
from queries import query_movie_with_id

app = Flask(__name__)

PORT = 3004
HOST = '0.0.0.0'
movie_graphql_service_url = "http://127.0.0.1:3001/graphql"

with open('./data/users.json', "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users", methods=['GET'])
def get_json():
    return make_response(jsonify(users), 200)


# Setup the gRPC channel and stub
channel = grpc.insecure_channel('localhost:3002')
stub = booking_pb2_grpc.BookingStub(channel)


def get_booking_by_user_id(stub, userid):
    request = booking_pb2.BookingUserId(userid=userid)
    booking = stub.GetBookingByUserID(request)
    return booking


def get_list_bookings(stub):
    allbookings = stub.GetListBookings(booking_pb2.Empty())
    for booking in allbookings:
        # Print the UserID and associated booking details
        print("Booking for UserID:", booking.userid)
        for date_data in booking.dates:
            print("  Date:", date_data.date)
            if date_data.movies:
                print("    Movies:")
                for movie in date_data.movies:
                    print("      -", movie.movie)
            else:
                print("    No movies booked for this date.")
        print()


@app.route("/user_info/<userid>", methods=["GET"])
def get_bookings_details(userid):
    booking_response = get_booking_by_user_id(stub, userid)
    response = []
    for date_data in booking_response.dates:
        movies_details = []
        for movie in date_data.movies:
            graphql_response = requests.post(movie_graphql_service_url, json={'query': query_movie_with_id(movie.movie)})
            movie_data = graphql_response.json()['data']['movie_with_id']
            movies_details.append(movie_data)
        response.append({'date': date_data.date, 'movies': movies_details})
    return make_response(jsonify(response), 200)


@app.route("/users/<userid>/<date>", methods=['GET'])
def get_movies_for_user_and_date(userid, date):
    try:
        booking_response = get_booking_by_user_id(stub, userid)
        result = []
        for date_data in booking_response.dates:
            if date_data.date == date:
                for movie in date_data.movies:
                    result.append(movie.movie)
        if not result:
            return make_response(jsonify({"error": "No reservations for this date"}), 404)
        return make_response(jsonify(result), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
