import grpc

from auth.src.app.services.user_service import UserService
from integration.messages import user_pb2_grpc, user_pb2
from app_grpc import app_grpc

class UserServices(user_pb2_grpc.UserServicer):
    def GetUser(self, request, context):
        if request.id:
            with app_grpc.app_context():
                roles = UserService().get_user_grpc(request.id)
                if roles:
                    return user_pb2.RoleList(
                        role=roles
                    )
                message = 'User ID not found'
                context.set_details(message)
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return user_pb2.RoleList()
        msg = 'Must pass ID'
        context.set_details(msg)
        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
        return user_pb2.RoleList()