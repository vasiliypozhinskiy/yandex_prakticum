from typing import List
import json

from app.views.models.auth import AuthReqView, AuthRespView
from app.models.db_models import User as DBUserModel
from app.utils.utils import check_password
from app.utils.exceptions import UnExistingLogin, InvalidToken, AccessDenied
from app.services.auth_services.jwt_service import JWT_SERVICE, AccessPayload
from app.services.auth_services.storages import REF_TOK_STORAGE
from app.services.auth_services.black_list import REVOKED_ACCESS, LOG_OUT_ALL


class AuthService:

    @staticmethod
    def login(request_data: AuthReqView) -> AuthRespView:
        try:
            login_data = AuthReqView.parse_obj(request_data)
        except Exception as err:
            return err.messages, 400

        creds_from_storage = DBUserModel.query.filter_by(login=login_data.login).first()
        if creds_from_storage is None:
            raise UnExistingLogin

        if check_password(
            password=login_data.password, hashed_password=creds_from_storage.password
        ): 

            # TODO write login info to relation db
            access_token, refresh_token = JWT_SERVICE.generate_tokens(
                user_id=creds_from_storage.id,
            )
            REF_TOK_STORAGE.add_token(refresh_token)
            return AuthRespView(access_token=access_token, refresh_token=refresh_token)
        else:
            raise AccessDenied

    @staticmethod
    def logout(access_token: str):
        payload = JWT_SERVICE.get_access_payload(access_token)
        if payload is not None:
            REVOKED_ACCESS.add(access_token) 
        else:
            raise InvalidToken
    
    @staticmethod
    def logout_all(access_token: str):
        payload = JWT_SERVICE.get_access_payload(access_token)
        if payload is not None:
            LOG_OUT_ALL.add(access_token)
        else:
            raise AccessDenied
    
    @staticmethod
    def authorize(access_token: str) -> List[str]:
        payload = JWT_SERVICE.get_access_payload(access_token)
        if payload is not None:
            if REVOKED_ACCESS.is_ok(access_token):
                if LOG_OUT_ALL.is_ok(access_token):
                    return payload.roles
        raise InvalidToken

AUTH_SERVICE = AuthService()