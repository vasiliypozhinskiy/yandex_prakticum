from typing import Optional

import grpc

import auth_pb2_grpc
import auth_pb2
from api.v1.exceptions import InvalidToken


def is_superuser(access_token: Optional[str] = None):
    if access_token is None:
        return False
    try:
        with grpc.insecure_channel('auth:50051') as channel:
            stub = auth_pb2_grpc.AuthStub(channel)
            response = stub.Authorize(
                auth_pb2.AuthorizeRequest(),
                metadata=(
                    ('access_token', access_token),
                )
            )
    # this is gracefull degradation
    except grpc.RpcError as err:
        if err.code() == grpc.StatusCode.UNAUTHENTICATED:
            raise InvalidToken
        raise err

    return response.is_superuser
