
import grpc

from app.services.auth_services.auth_services import AUTH_SERVICE
from app.services.user_service import UserService as UserServiceGrpc
from app.views.user_view import UserView
from integration.messages import role_pb2_grpc, role_pb2
from main import app_grpc
from loguru import logger

class RoleService(role_pb2_grpc.RoleServicer):
    def GetToken(self, request, context):
        app_grpcs = app_grpc()
        if request.login and request.password:
            print('tis')
            with app_grpcs.app_context():
                user_login = AUTH_SERVICE.login(request.login,
                                                request.password,
                                                request.headers.get('User-Agent')
                                                )
                if user_login:
                    logger.info(user_login)
                    logger.debug(role_pb2.TokenResponse)
