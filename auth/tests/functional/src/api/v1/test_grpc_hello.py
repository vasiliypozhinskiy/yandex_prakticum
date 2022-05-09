import grpc
import pytest

import hello_world_pb2
import hello_world_pb2_grpc

# All test coroutines will be treated as marked with this decorator.
pytestmark = pytest.mark.asyncio


async def test_grpc_hello(make_request):
    with grpc.insecure_channel('auth:50051') as channel:
        stub = hello_world_pb2_grpc.GreetingsStub(channel)
        response = stub.Greet(hello_world_pb2.GreetingRequest(user_id=1))
        assert response.greetings == 'hello' 