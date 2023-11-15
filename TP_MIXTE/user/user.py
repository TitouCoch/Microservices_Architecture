from flask import Flask, jsonify, make_response, request
import requests
import json
import grpc
import booking_pb2
import booking_pb2_grpc
from queries import query_movie_with_id, query_movie_name_with_id, query_all_movies, mutation_add_movie, \
    mutation_update_movie, mutation_delete_movie, query_movie_with_title

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

# USER


@app.route("/users", methods=['GET'])
def get_users():
    return make_response(jsonify(users), 200)


@app.route("/user/user_by_id/<userid>", methods=['GET'])
def get_user_by_id(userid):
    user = next((user for user in users if user["id"] == userid), None)
    if user:
        return make_response(jsonify(user), 200)
    else:
        return make_response(jsonify({"message": "User not found"}), 404)


@app.route("/user/add_user/<userid>", methods=['POST'])
def add_user(userid):
    req = request.get_json()
    for user in users:
        if str(user["id"]) == str(userid):
            return make_response(jsonify({"error": "User ID already exists"}),409)
    users.append(req)
    res = make_response(jsonify({"message": "user added"}), 200)
    return res


@app.route("/user/update_user_name/<userid>/<name>", methods=['PUT'])
def update_user_name(userid, name):
    for user in users:
        if str(user["id"]) == str(userid):
            user["name"] = name
            res = make_response(jsonify(user), 200)
            return res
    res = make_response(jsonify({"error": "user ID not found"}), 201)
    return res


@app.route("/user/delete_user/<userid>", methods=['DELETE'])
def delete_user(userid):
    for user in users:
        if user["id"] == userid:
            users.remove(user)
            return make_response(jsonify(user), 200)
    res = make_response(jsonify({"error": "user ID not found"}), 400)
    return res


# MOVIE


@app.route("/user/movies", methods=["GET"])
def get_movies():
    movies_response = requests.post(movie_graphql_service_url, json={'query': query_all_movies()})
    if movies_response.status_code != 200:
        return make_response(jsonify({"error": "Movie data not found"}), 404)
    movies_data = movies_response.json()
    return movies_data


@app.route("/user/movie_by_id/<movieid>", methods=["GET"])
def get_movie_by_id(movieid):
    movies_response = requests.post(movie_graphql_service_url, json={'query': query_movie_with_id(movieid)})
    if movies_response.status_code != 200:
        return make_response(jsonify({"error": "Movie data not found"}), 404)
    movies_data = movies_response.json()
    return movies_data


@app.route("/user/movie_name_by_id/<movieid>", methods=["GET"])
def get_movie_name_by_id(movieid):
    movies_response = requests.post(movie_graphql_service_url, json={'query': query_movie_name_with_id(movieid)})
    if movies_response.status_code != 200:
        return make_response(jsonify({"error": "Movie data not found"}), 404)
    movies_data = movies_response.json()
    movie_title = movies_data["data"]["movie_with_id"]["title"]
    print(movie_title)
    return {"title": movie_title}


@app.route("/user/add_movie", methods=["POST"])
def add_movie():
    movie_data = request.get_json()
    existing_movie_response = requests.post(movie_graphql_service_url, json={'query': query_movie_with_title(movie_data['title'])})
    if existing_movie_response.status_code == 200 and existing_movie_response.json().get("data", {}).get("movie_with_title"):
        return make_response(jsonify({"error": "Movie already exists"}), 409)
    response = requests.post(movie_graphql_service_url, json={'query': mutation_add_movie(movie_data)})
    if response.status_code != 200:
        return make_response(jsonify({"error": "Failed to add movie"}), response.status_code)
    res = make_response(jsonify({"message": "movie added"}), 200)
    return res


@app.route("/user/update_movie/<movieid>", methods=["POST"])
def update_movie(movieid):
    movie_data = request.get_json()
    new_rating = movie_data.get("rating")
    response = requests.post(movie_graphql_service_url,json={'query': mutation_update_movie(movieid, new_rating)})
    if response.status_code != 200:
        return make_response(jsonify({"error": "Failed to update movie"}), response.status_code)
    return make_response(jsonify({"message": "Movie updated successfully"}), 200)


@app.route("/user/delete_movie/<movieid>", methods=["POST"])
def delete_movie(movieid):
    response = requests.post(movie_graphql_service_url, json={'query': mutation_delete_movie(movieid)})
    if response.status_code != 200:
        return make_response(jsonify({"error": "Failed to delete movie"}), response.status_code)
    return make_response(jsonify({"message": "Movie deleted successfully"}), 200)


# BOOKING


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


# TIME

@app.route("/user/showtimes", methods=['GET'])
def get_showtimes():
    allshowtimes = stub.GetListShowtimes(booking_pb2.EmptyBooking())
    response = []
    for booking in allshowtimes.bookings:
        list_movies = []
        for movie in booking.movies:
            movie_name = get_movie_name_by_id(movie.movie)
            list_movies.append(movie_name['title'])
        response.append({'date': booking.date,'movies': list_movies})
    return make_response(jsonify(response), 200)


@app.route("/user/showtime_by_movie/<movieid>", methods=['GET'])
def get_showtime_by_movieid(movieid):
    allshowtimes = stub.GetShowtimeByMovie(booking_pb2.Movie(movie=movieid))
    response = []
    dates = []
    for date in allshowtimes.dates:
        dates.append(date.date)
    movie_title = get_movie_name_by_id(allshowtimes.movie.movie)['title']
    response.append({'movie': movie_title,'dates': dates})
    return make_response(jsonify(response), 200)


@app.route("/user/showtime_by_date/<date>", methods=['GET'])
def get_showtime_by_date(date):
    allshowtimes = stub.GetShowtimeByDate(booking_pb2.Date(date=date))
    response = []
    movies = []
    for movie in allshowtimes.movies:
        movie_name = get_movie_name_by_id(movie.movie)
        movies.append(movie_name['title'])
    response.append({'date': allshowtimes.date,'movies': movies})
    return make_response(jsonify(response), 200)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
