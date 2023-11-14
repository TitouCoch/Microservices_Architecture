import json
import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc


# Setup the gRPC channel and stub
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
    print(showtime_dates_response)
    dates = []
    for date in showtime_dates_response.dates:
        dates.append(booking_pb2.Date(date=date))
    showtime_by_movie_data = booking_pb2.ShowtimeByMovieData(movie=request,dates=dates)
    return showtime_by_movie_data


class BookingServicer(booking_pb2_grpc.BookingServicer):

    #get_showtime_by_date(stub, "20151201")

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetBookingByUserID(self, request, context):
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
        for booking in self.db:
            date_data_list = []
            for date_entry in booking['dates']:
                movie_list = [booking_pb2.Movie(movie=movie_id) for movie_id in date_entry['movies']]
                date_data = booking_pb2.DateData(date=date_entry['date'], movies=movie_list)
                date_data_list.append(date_data)
            yield booking_pb2.BookingData(userid=booking['userid'], dates=date_data_list)

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

