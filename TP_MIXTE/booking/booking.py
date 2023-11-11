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
    print(allshowtimes)
    for showtime in allshowtimes:
        print("Showtime %s" % showtime)


def get_showtime_by_date(_stub, date):
    showtime_date_request = showtime_pb2.ShowtimeDate(date=date)
    try:
        showtime_data = _stub.GetShowtimeByDate(showtime_date_request)
        movie_ids = [movie.movie for movie in showtime_data.movies]
        print("Showtime data for date:", showtime_data.date)
        print("Movies:", movie_ids)
    except grpc.RpcError as e:
        print("Rpc request failed")


def get_showtime_by_movie(_stub, movie):
    showtime_movie_request = showtime_pb2.ShowtimeMovie(movie=movie)
    try:
        showtime_dates_response = _stub.GetShowtimeByMovie(showtime_movie_request)
        response_message = f"Movie ID {movie} available showtime dates: {list(showtime_dates_response.dates)}"
        print(response_message)
    except grpc.RpcError as e:
        print("Rpc request failed")


class BookingServicer(booking_pb2_grpc.BookingServicer):

    #get_list_showtime(stub)
    #get_showtime_by_date(stub, "20151201")
    #get_showtime_by_movie(stub, "39ab85e5-5e8e-4dc5-afea-65dc368bd7ab")


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


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('localhost:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

