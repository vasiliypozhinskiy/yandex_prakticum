import json

import grpc

from app.views.user_view import UserView
from integration.messages import user_pb2_grpc, user_pb2
from main import app


class UserServices(user_pb2_grpc.UserServicer):
    def GetUser(self, request, context):
        if request.id:
            with app.app_context():
                user = UserView()._get_user(request.id)
                user_decode = json.loads(user.response[0].decode('utf-8'))
                if user:
                    return user_pb2.UserResponse(
                        login=user_decode['login'],
                        email=user_decode['email'],
                        first_name=user_decode['first_name'],
                        last_name=user_decode['last_name'],
                        birth_data=user_decode['birthdate']
                    )
                message = 'User ID not found'
                context.set_details(message)
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return user_pb2.UserResponse
        msg = 'Must pass ID'
        context.set_details(msg)
        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
        return user_pb2.UserResponse()