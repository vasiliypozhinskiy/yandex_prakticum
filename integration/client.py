import grpc
#
from messages import user_pb2, user_pb2_grpc

def get_user(id: str):
    channel = grpc.insecure_channel("127.0.0.1:50051")
    client = user_pb2_grpc.UserStub(channel)
    try:
        response = client.GetUser(user_pb2.UserRequest(id=id))
    except grpc.RpcError as err:
        raise err
    return response