import grpc
#
from messages import role_pb2, role_pb2_grpc
from messages import user_pb2, user_pb2_grpc

def run():
    with grpc.insecure_channel("127.0.0.1:50051") as channel:
        client = user_pb2_grpc.UserStub(channel)
        response = client.GetUser(user_pb2.UserRequest(id=id))
        print(response.message)

if __name__ == "__main__":
    run()





# def get_user(id):
#     channel = grpc.insecure_channel("127.0.0.1:50051")
#     client = user_pb2_grpc.UserStub(channel)
#     response = client.GetUser(user_pb2.UserRequest(id=id))
#     print(response)
#     if response:
#         return response
#     return None
# get_user('b1442bd3-a0ed-4c4b-9e08-6a5a046083b5')

