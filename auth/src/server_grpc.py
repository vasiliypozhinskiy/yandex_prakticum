from concurrent import futures

import grpc

import hello_world_pb2_grpc as hello_world_pb2_grpc
import hello_world_pb2 as hello_world_pb2


class Greeter(hello_world_pb2_grpc.GreetingsServicer):
    def Greet(self, request, context):
        print("Got request " + str(request), flush=True)
        return hello_world_pb2.GreetingResponse(greetings="hello")


def server():
    _server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    hello_world_pb2_grpc.add_GreetingsServicer_to_server(Greeter(), _server)
    _server.add_insecure_port('[::]:50051')
    print("gRPC starting", flush=True)
    _server.start()
    _server.wait_for_termination()


server()
