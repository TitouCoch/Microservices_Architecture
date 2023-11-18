import json
import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc

channel = grpc.insecure_channel('localhost:3003')
stub = showtime_pb2_grpc.ShowtimeStub(channel)


def get_list_showtime(_stub):
    allshowtimes = _stub.GetListShowtimes(showtime_pb2.EmptyShowTime())
    bookings_response = []
    for showtime in allshowtimes:
        movie_list = []
        for movie in showtime.movies:
            movie_list.append(booking_pb2.Movie(movie=movie.movie))
        bookings_response.append(booking_pb2.DateData(date=showtime.date, movies=movie_list))
    return booking_pb2.ShowtimesDataByDate(bookings=bookings_response)


def get_showtime_by_date(_stub, date):
    request = booking_pb2.Date(date=date.date)
    showtime_movies_response = _stub.GetShowtimeByDate(request)
    movies = []
    for movie in showtime_movies_response.movies:
        movies.append(booking_pb2.Movie(movie=movie.movie))
    showtime_by_date_data = booking_pb2.DateData(date=date.date, movies=movies)
    return showtime_by_date_data


def get_showtime_by_movie(_stub, movie):
    request = booking_pb2.Movie(movie=movie.movie)
    showtime_dates_response = _stub.GetShowtimeByMovie(request)
    dates = []
    for date in showtime_dates_response.dates:
        dates.append(booking_pb2.Date(date=date))
    showtime_by_movie_data = booking_pb2.ShowtimeByMovieData(movie=request, dates=dates)
    return showtime_by_movie_data


class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    # BOOKING
    def GetBookingByUserID(self, request, context):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]
        for booking in self.db:
            if booking['userid'] == request.userid:
                date_data_list = []
                for date_entry in booking['dates']:
                    movie_list = [booking_pb2.Movie(movie=movie_id) for movie_id in date_entry['movies']]
                    date_data = booking_pb2.DateData(date=date_entry['date'], movies=movie_list)
                    date_data_list.append(date_data)
                return booking_pb2.BookingData(userid=booking['userid'], dates=date_data_list)
        return booking_pb2.BookingData(userid=request.userid)

    def GetListBookings(self, request, context):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]
        for booking in self.db:
            date_data_list = []
            for date_entry in booking['dates']:
                movie_list = [booking_pb2.Movie(movie=movie_id) for movie_id in date_entry['movies']]
                date_data = booking_pb2.DateData(date=date_entry['date'], movies=movie_list)
                date_data_list.append(date_data)
            yield booking_pb2.BookingData(userid=booking['userid'], dates=date_data_list)

    def AddBooking(self, request, context):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)
        new_booking = {
            "userid": request.userid,
            "dates": [
                {"date": date_data.date, "movies": [movie.movie for movie in date_data.movies]}
                for date_data in request.dates
            ]
        }
        user_exists = False
        for booking in self.db["bookings"]:
            if booking["userid"] == new_booking["userid"]:
                user_exists = True
                for new_date in new_booking["dates"]:
                    existing_date = next((d for d in booking["dates"] if d["date"] == new_date["date"]), None)
                    if existing_date:
                        existing_date["movies"].extend(
                            movie for movie in new_date["movies"] if movie not in existing_date["movies"])
                    else:
                        booking["dates"].append(new_date)
                break
        if not user_exists:
            self.db["bookings"].append(new_booking)
        with open('{}/data/bookings.json'.format("."), "w") as jsf:
            json.dump(self.db, jsf)
        return booking_pb2.BookingResponse(success=True, message="Booking added successfully")

    def UpdateBooking(self, request, context):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)
        updated = False
        for booking in self.db["bookings"]:
            if booking["userid"] == request.userid:
                for update_date in request.dates:
                    for date in booking["dates"]:
                        if date["date"] == update_date.date:
                            date["movies"] = [movie.movie for movie in update_date.movies]
                            updated = True
                            break
        if updated:
            with open('{}/data/bookings.json'.format("."), "w") as jsf:
                json.dump(self.db, jsf)
            return booking_pb2.BookingResponse(success=True, message="Booking updated successfully")
        else:
            return booking_pb2.BookingResponse(success=False, message="Booking not found for update")

    def DeleteBooking(self, request, context):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)
        booking_index = next(
            (i for i, booking in enumerate(self.db["bookings"]) if booking["userid"] == request.userid), None)
        if booking_index is not None:
            del self.db["bookings"][booking_index]
            with open('{}/data/bookings.json'.format("."), "w") as jsf:
                json.dump(self.db, jsf)
            return booking_pb2.BookingResponse(success=True, message="Booking deleted successfully")
        else:
            return booking_pb2.BookingResponse(success=False, message="Booking not found for deletion")

    # TIME

    def GetListShowtimes(self, request, context):
        return get_list_showtime(stub)

    def GetShowtimeByDate(self, request, context):
         return get_showtime_by_date(stub, request)

    def GetShowtimeByMovie(self, request, context):
        return get_showtime_by_movie(stub, request)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('localhost:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
