from concurrent import futures

import grpc

import hello_world_pb2_grpc as hello_world_pb2_grpc
import hello_world_pb2 as hello_world_pb2


class Auth(hello_world_pb2_grpc.AuthServicer):
    def Greet(self, request, context):
        print("Got request " + str(request), flush=True)
        return hello_world_pb2.GreetingResponse(greetings="hello")

    def Authorize(self, request, context):
        return hello_world_pb2.AuthorizeResponse(
            roles=['lol', 'kek'],
            is_superuser=False,
        )


def server():
    _server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    hello_world_pb2_grpc.add_AuthServicer_to_server(Auth(), _server)

    _server.add_insecure_port('[::]:50051')
    print("gRPC starting", flush=True)
    _server.start()
    _server.wait_for_termination()


server()
