import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json


class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    def GetListShowtimes(self, request, context):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]
        for showtime in self.db:
            movie_messages = [showtime_pb2.Movie_list(movie=movie_id) for movie_id in showtime['movies']]
            yield showtime_pb2.ShowtimeData(date=showtime['date'], movies=movie_messages)

    def GetShowtimeByDate(self, request, context):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]
        for showtime in self.db:
            if showtime['date'] == request.date:
                movie_messages = [showtime_pb2.Movie_list(movie=movie_id) for movie_id in showtime['movies']]
                return showtime_pb2.ShowtimeData(date=showtime['date'], movies=movie_messages)
        return showtime_pb2.ShowtimeData()

    def GetShowtimeByMovie(self, request, context):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]
        dates_set = set()
        for showtime in self.db:
            if request.movie in showtime['movies']:
                dates_set.add(showtime['date'])
        dates_list = sorted(list(dates_set))
        return showtime_pb2.ShowtimeDates(dates=dates_list)

    def AddShowtime(self, request, context):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]
        date_exists = False
        for showtime in self.db:
            if showtime['date'] == request.date:
                date_exists = True
                for movie in request.movies:
                    if movie.movie not in showtime['movies']:
                        showtime['movies'].append(movie.movie)
                break
        if not date_exists:
            new_showtime = {"date": request.date, "movies": [movie.movie for movie in request.movies]}
            self.db.append(new_showtime)
        with open('{}/data/times.json'.format("."), "w") as jsf:
            json.dump({"schedule": self.db}, jsf)
        return showtime_pb2.OperationStatus(success=True, message="Showtime ajouté ou mis à jour")

    def UpdateShowtime(self, request, context):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]
        date_exists = False
        for showtime in self.db:
            if showtime['date'] == request.date:
                date_exists = True
                showtime['movies'] = [movie.movie for movie in request.movies]
                break
        if not date_exists:
            return showtime_pb2.OperationStatus(success=False, message="Date non trouvée")
        with open('{}/data/times.json'.format("."), "w") as jsf:
            json.dump({"schedule": self.db}, jsf)
        return showtime_pb2.OperationStatus(success=True, message="Showtime mis à jour")

    def DeleteShowtime(self, request, context):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]
        self.db = [showtime for showtime in self.db if showtime['date'] != request.date]
        with open('{}/data/times.json'.format("."), "w") as jsf:
            json.dump({"schedule": self.db}, jsf)
        return showtime_pb2.OperationStatus(success=True, message="Showtime supprimé")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('0.0.0.0:3003')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
