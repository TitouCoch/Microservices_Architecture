from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
import requests
import grpc
import booking_pb2
import booking_pb2_grpc
from queries import query_movie_with_id, query_movie_name_with_id, query_all_movies, mutation_add_movie, \
    mutation_update_movie, mutation_delete_movie, query_movie_with_title
from utilities import UserRepository

app = Flask(__name__)
# Headers to allow CORS
cors = CORS(app, resources={r"/*": {"origins": "*"}})

PORT = 3004
HOST = '0.0.0.0'
movie_graphql_service_url = "http://movie:3001/graphql"

channel = grpc.insecure_channel('booking:3002')
stub = booking_pb2_grpc.BookingStub(channel)

userRepository = UserRepository()


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


# USER

@app.route("/users", methods=['GET'])
def get_users():
    return make_response(jsonify(userRepository.get_users()), 200)


@app.route("/users/<userid>", methods=['GET'])
def get_user_by_id(userid):
    user = userRepository.get_user_by_id(userid)
    if user:
        return make_response(jsonify(user), 200)
    else:
        return make_response(jsonify({"message": "User not found"}), 404)


@app.route("/users", methods=['POST'])
def add_user():
    req = request.get_json()
    new_user = userRepository.add_user(req)
    return make_response(jsonify(new_user), 200)


@app.route("/users/<userid>", methods=['PATCH'])  # partial update so its a patch
def update_user_name(userid):
    name = request.get_json()["name"]
    user = userRepository.update_user_name(userid, name)
    if user:
        return make_response(jsonify(user), 200)
    else:
        return make_response(jsonify({"error": "User not found"}), 400)


@app.route("/users/<userid>", methods=['DELETE'])
def delete_user(userid):
    if userRepository.delete_user(userid):
        return make_response(jsonify({"message": "User deleted successfully"}), 200)
    return make_response(jsonify({"error": "User not found"}), 400)


# MOVIE
@app.route("/movies", methods=["GET"])
def get_movies():
    movies_response = requests.post(movie_graphql_service_url, json={'query': query_all_movies()})
    if movies_response.status_code != 200:
        return make_response(jsonify({"error": "Movie data not found"}), 404)
    response = movies_response.json()['data']['all_movies']
    return make_response(jsonify(response), 200)


@app.route("/movies/<movieid>", methods=["GET"])
def get_movie_by_id(movieid):
    movies_response = requests.post(movie_graphql_service_url, json={'query': query_movie_with_id(movieid)})
    if movies_response.status_code != 200:
        return make_response(jsonify({"error": "Movie not found"}), 404)
    movies_data = movies_response.json()
    return movies_data


def get_movie_name_by_id(movieid):
    movies_response = requests.post(movie_graphql_service_url, json={'query': query_movie_name_with_id(movieid)})
    if movies_response.status_code != 200 or not movies_response.json().get('data', {}).get('movie_with_id'):
        return make_response(jsonify({"error": "Movie not found"}), 400)
    movie_title = movies_response.json()["data"]["movie_with_id"]["title"]
    return jsonify(movie_title)


def is_movie_valid(movie_id):
    response = get_movie_name_by_id(movie_id)
    return response.status_code == 200


@app.route("/movies", methods=["POST"])
def add_movie():
    movie_data = request.get_json()
    existing_movie_response = requests.post(movie_graphql_service_url,
                                            json={'query': query_movie_with_title(movie_data['title'])})
    if (existing_movie_response.status_code == 200 and existing_movie_response.json()
            .get("data", {}).get("movie_with_title")):
        return make_response(jsonify({"error": "Movie already exists"}), 409)
    response = requests.post(movie_graphql_service_url, json={'query': mutation_add_movie(movie_data)})
    if response.status_code != 200:
        return make_response(jsonify({"error": "Failed to add movie"}), response.status_code)
    new_movie = response.json()['data']['add_movie']
    return make_response(jsonify(new_movie), 200)


@app.route("/movies/<movieid>", methods=["PATCH"])
def update_movie(movieid):
    movie_data = request.get_json()
    new_rating = movie_data.get("rating")
    response = requests.post(movie_graphql_service_url, json={'query': mutation_update_movie(movieid, new_rating)})
    movie = response.json()['data']['update_movie_rate']
    if response.status_code != 200:
        return make_response(jsonify({"error": "Failed to update movie"}), response.status_code)
    return make_response(jsonify(movie), 200)


@app.route("/movies/<movieid>", methods=["DELETE"])
def delete_movie(movieid):
    response = requests.post(movie_graphql_service_url, json={'query': mutation_delete_movie(movieid)})
    if response.status_code != 200:
        return make_response(jsonify({"error": "Failed to delete movie"}), response.status_code)
    return make_response(jsonify({"message": "Movie deleted successfully"}), 200)


# BOOKING


@app.route("/users/<userid>/bookings", methods=["GET"])
def get_booking_by_user_id(userid):
    date = request.args.get('date')

    # Build GRPC Object to send to booking service
    response = booking_pb2.BookingUserId(userid=userid)
    # Make GRPC call to booking service
    booking = stub.GetBookingByUserID(response)
    # Build response object
    booking_details = {"userid": booking.userid, "dates": []}
    for date_data in booking.dates:
        if date and date_data.date != date:
            continue
        date_details = {"date": date_data.date, "movies": [movie.movie for movie in date_data.movies]}
        booking_details["dates"].append(date_details)

    return booking_details


@app.route("/users/<userid>/bookings", methods=["POST"])
def add_booking_to_user(userid):
    booking_data = request.get_json()
    user_id = userid
    movie_id = booking_data['movieId']
    date = booking_data['date']
    # Build grpc object to send to booking service
    grpc_request = booking_pb2.BookingData(userid=user_id, dates=[
        booking_pb2.DateData(date=date, movies=[booking_pb2.Movie(movie=movie_id)])])
    response = stub.AddBooking(grpc_request)
    return jsonify({"success": response.success, "message": response.message})


@app.route("/users/<userid>/bookings", methods=["DELETE"])
def delete_booking_by_user_id(userid):
    # check args
    movieid = request.args.get('movieId')
    date = request.args.get('date')
    if not movieid or not date:
        return make_response(jsonify({"error": "Movie id or date not provided"}), 400)
    # Build grpc object to send to booking service
    grpc_request = booking_pb2.BookingData(userid=userid, dates=[
        booking_pb2.DateData(date=date, movies=[booking_pb2.Movie(movie=movieid)])])
    response = stub.DeleteBooking(grpc_request)
    return jsonify({"success": response.success, "message": response.message})


@app.route("/bookings", methods=["GET"])
def get_list_bookings():
    # Make call to booking service
    allbookings = stub.GetListBookings(booking_pb2.EmptyBooking())
    # Map the response object from grpc to a json response object
    bookings_list = []
    for booking in allbookings:
        booking_details = {"userid": booking.userid, "dates": []}
        for date_data in booking.dates:
            date_details = {"date": date_data.date, "movies": []}
            if date_data.movies:
                for movie in date_data.movies:
                    date_details["movies"].append(movie.movie)
            booking_details["dates"].append(date_details)
        bookings_list.append(booking_details)
    return jsonify(bookings_list)


@app.route("/users/<userid>/details", methods=["GET"])
def get_bookings_details(userid):
    # get bookings from booking service using grpc
    booking_response = get_booking_by_user_id(userid)

    # map booking response to a response object with movies details for each date
    response = []
    for date_data in booking_response['dates']:
        movies_details = []
        for movie in date_data['movies']:
            # retrieve movie details from movie service by using grapqhl query
            graphql_response = requests.post(movie_graphql_service_url,
                                             json={'query': query_movie_with_id(movie)})
            movie_data = graphql_response.json()['data']['movie_with_id']
            movies_details.append(movie_data)
        response.append({'date': date_data['date'], 'movies': movies_details})
    return make_response(jsonify(response), 200)


# TIME

@app.route("/showtimes", methods=['GET'])
def get_showtimes():
    # check args
    date = request.args.get('date')
    if date:
        return get_showtime_by_date(date)

    # make grpc call to Showtime Service
    allshowtimes = stub.GetListShowtimes(booking_pb2.EmptyBooking())

    # Build object response
    response = []
    for booking in allshowtimes.bookings:
        list_movies = []
        for movie in booking.movies:
            movie_name = get_movie_name_by_id(movie.movie)
            list_movies.append(movie_name.json)
        response.append({'date': booking.date, 'movies': list_movies})
    return make_response(jsonify(response), 200)


def get_showtime_by_date(date):
    # Make grpc call to Showtime service
    allshowtimes = stub.GetShowtimeByDate(booking_pb2.Date(date=date))

    # build response object
    response = []
    movies = []
    for movie in allshowtimes.movies:
        movie_name = get_movie_name_by_id(movie.movie)
        movies.append(movie_name.json)
    response.append({'date': allshowtimes.date, 'movies': movies})
    return make_response(jsonify(response), 200)


@app.route("/movies/<movieid>/showtimes", methods=['GET'])
def get_showtime_by_movieid(movieid):
    allshowtimes = stub.GetShowtimeByMovie(booking_pb2.Movie(movie=movieid))
    response = []
    dates = []
    for date in allshowtimes.dates:
        dates.append(date.date)
    movie_title = get_movie_name_by_id(allshowtimes.movie.movie).json
    response.append({'movie': movie_title, 'dates': dates})
    return make_response(jsonify(response), 200)


@app.route("/showtimes", methods=['POST'])
def add_showtime():
    showtime_data = request.get_json()
    date = showtime_data['date']
    movie_ids = showtime_data['movie_ids']
    valid_movie_ids = [movie_id for movie_id in movie_ids if is_movie_valid(movie_id)]
    movie_list = [booking_pb2.Movie(movie=movie_id) for movie_id in valid_movie_ids]
    date_data = booking_pb2.DateData(date=date, movies=movie_list)
    response = stub.Add_Showtime(date_data)
    response_dict = {"success": response.success, "message": response.message}
    return make_response(jsonify(response_dict), 200)


@app.route("/showtimes", methods=['PUT'])
def update_showtime():
    # Retrieve data from request
    showtime_data = request.get_json()
    date = showtime_data['date']
    if not date:  # if no date provided in request
        return make_response(jsonify({"error": "No date provided"}), 400)

    movie_ids = showtime_data['movie_ids']
    valid_movie_ids = [movie_id for movie_id in movie_ids if is_movie_valid(movie_id)]
    movie_list = [booking_pb2.Movie(movie=movie_id) for movie_id in valid_movie_ids]
    date_data = booking_pb2.DateData(date=date, movies=movie_list)
    response = stub.Update_Showtime(date_data)
    response_dict = {"success": response.success, "message": response.message}
    return make_response(jsonify(response_dict), 200)


@app.route("/showtimes", methods=['DELETE'])
def delete_showtime_from_booking():
    date = request.args.get('date')
    if not date:  # if no date provided
        return make_response(jsonify({"error": "No date provided"}), 400)
    date_obj = booking_pb2.Date(date=date)
    # make request to
    response = stub.Delete_Showtime(date_obj)
    response_dict = {"success": response.success, "message": response.message}
    return make_response(jsonify(response_dict), 200)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
