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
movie_graphql_service_url = ("http://127.0.0.1:3001/graphql")
channel = grpc.insecure_channel('localhost:3002')
stub = booking_pb2_grpc.BookingStub(channel)

with open('./data/users.json', "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users", methods=['GET'])
def get_json():
    return make_response(jsonify(users), 200)


@app.route("/user/booking/<userid>", methods=["GET"])
def get_booking_by_user_id(userid):
    request = booking_pb2.BookingUserId(userid=userid)
    booking = stub.GetBookingByUserID(request)
    booking_details = {"userid": booking.userid,"dates": []}
    for date_data in booking.dates:
        date_details = {"date": date_data.date,"movies": [movie.movie for movie in date_data.movies]}
        booking_details["dates"].append(date_details)
    return jsonify(booking_details)


@app.route("/user/list_bookings", methods=["GET"])
def get_list_bookings():
    allbookings = stub.GetListBookings(booking_pb2.EmptyBooking())
    bookings_list = []
    for booking in allbookings:
        booking_details = {"userid": booking.userid,"dates": []}
        for date_data in booking.dates:
            date_details = {"date": date_data.date, "movies": []}
            if date_data.movies:
                for movie in date_data.movies:
                    date_details["movies"].append(movie.movie)
            booking_details["dates"].append(date_details)
        bookings_list.append(booking_details)
    return jsonify(bookings_list)


@app.route("/user/user_info/<userid>", methods=["GET"])
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


@app.route("/user/<userid>/<date>", methods=['GET'])
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


@app.route("/user/showtimes", methods=['GET'])
def get_showtimes():
    allshowtimes = stub.GetListShowtimes(booking_pb2.EmptyBooking())
    response = []
    for booking in allshowtimes.bookings:
        list_movies = []
        for movie in booking.movies:
            list_movies.append(movie.movie)
        response.append({'date': booking.date,'movies': list_movies})
    return make_response(jsonify(response), 200)


@app.route("/user/showtime_by_movie/<movieid>", methods=['GET'])
def get_showtime_by_movieid(movieid):
    allshowtimes = stub.GetShowtimeByMovie(booking_pb2.Movie(movie=movieid))
    response = []
    dates = []
    for date in allshowtimes.dates:
        dates.append(date.date)
    response.append({'movie': allshowtimes.movie.movie,'dates': dates})
    return make_response(jsonify(response), 200)


@app.route("/user/showtime_by_date/<date>", methods=['GET'])
def get_showtime_by_date(date):
    allshowtimes = stub.GetShowtimeByDate(booking_pb2.Date(date=date))
    print(allshowtimes)
    response = []
    movies = []
    for movie in allshowtimes.movies:
        movies.append(movie.movie)
    response.append({'date': allshowtimes.date,'movies': movies})
    return make_response(jsonify(response), 200)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
