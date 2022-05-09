import grpc
import pytest
from http import HTTPStatus

import hello_world_pb2
import hello_world_pb2_grpc

# All test coroutines will be treated as marked with this decorator.
pytestmark = pytest.mark.asyncio


ACCESS_TOKEN = None
USER_ID = None
USER = {
  "email": "example@email.com",
  "first_name": "Ivan",
  "last_name": "Ivan",
  "login": "login",
  "birthdate": "2000-01-20",
  "password": "123qweQWE!@#",
}


async def test_grpc_hello(make_request):
    with grpc.insecure_channel('auth:50051') as channel:
        stub = hello_world_pb2_grpc.AuthStub(channel)
        response = stub.Greet(hello_world_pb2.GreetingRequest(user_id=1))
        assert response.greetings == 'hello'


async def test_user_create(make_request):
    global USER_ID
    global USER

    response = await make_request("post")(
        "user/",
        json=USER,
    )
    assert response.status == HTTPStatus.CREATED
    USER_ID = response.body["user_id"]


async def test_login(make_request):
    global ACCESS_TOKEN
    response = await make_request("post")(
        "login/",
        json={"login": "login", "password": "123qweQWE!@#"},
    )

    assert response.status == HTTPStatus.OK
    ACCESS_TOKEN = response.body['access_token']


async def test_check_authorized(make_request):
    global ACCESS_TOKEN
    with grpc.insecure_channel('auth:50051') as channel:
        stub = hello_world_pb2_grpc.AuthStub(channel)
        response = stub.Authorize(
            hello_world_pb2.AuthorizeRequest(
                access_token=ACCESS_TOKEN,
            )
        )
    assert response.roles == []


