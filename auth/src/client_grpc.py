import grpc

import hello_world_pb2
import hello_world_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:80') as channel:
        stub = hello_world_pb2_grpc.GreetingsStub(channel)
        response = stub.Greet(hello_world_pb2.GreetingRequest(user_id=1))
    print("Greeter client received following from server: " + response.greetings)  


run()
