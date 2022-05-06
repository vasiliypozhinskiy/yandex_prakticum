import grpc

from messages import role_pb2, role_pb2_grpc
from messages import user_pb2, user_pb2_grpc


def get_user(id):
    channel = grpc.insecure_channel("127.0.0.1:50051")
    client = user_pb2_grpc.UserStub(channel)
    response = client.GetUser(user_pb2.UserRequest(id=id))
    if response:
        return response
    return None
# get_user('968b0d89-adb3-4250-a596-de33aee38488')

def get_token(login, password):
    channel = grpc.insecure_channel("127.0.0.1:50051")
    client = role_pb2_grpc.RoleStub(channel)
    response = client.getAccess(role_pb2.LoginRequest(login=login, password=password))
    if response:
        print('ok')
        return response
    print('no ok')
get_token('login', '123qweQWE!@#')