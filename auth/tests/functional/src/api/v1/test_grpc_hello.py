import grpc
import pytest

import hello_world_pb2
import hello_world_pb2_grpc

# All test coroutines will be treated as marked with this decorator.
pytestmark = pytest.mark.asyncio


async def test_grpc_hello(make_request):
    with grpc.insecure_channel('auth:50051') as channel:
        stub = hello_world_pb2_grpc.AuthStub(channel)
        response = stub.Greet(hello_world_pb2.GreetingRequest(user_id=1))
        assert response.greetings == 'hello'


async def test_grpc_roles(make_request):
    with grpc.insecure_channel('auth:50051') as channel:
        stub = hello_world_pb2_grpc.AuthStub(channel)
        response = stub.Authorize(hello_world_pb2.AuthorizeRequest(user_id=1))
        assert not response.is_superuser
        assert response.roles == ['lol', 'kek']
