from functools import wraps
from typing import List, Optional
import uuid

from flask import request

from app.views.models.auth import AuthReqView, AuthRespView
from app.services.storage.storage import user_table, user_login_history_table
from app.utils.utils import check_password
from app.utils.exceptions import UnExistingLogin, InvalidToken, AccessDenied
from app.services.auth_services.jwt_service import JWT_SERVICE
from app.services.auth_services.storages import REF_TOK_STORAGE
from app.services.auth_services.black_list import REVOKED_ACCESS, LOG_OUT_ALL, ROLES_UPDATE


class AuthService:

    @staticmethod
    def login(request_data: AuthReqView, agent: str) -> AuthRespView:
        login_data = AuthReqView.parse_obj(request_data)

        creds_from_storage = user_table.read(filter={"login": login_data.login})
        print(creds_from_storage, flush=True)
        if creds_from_storage is None:
            raise UnExistingLogin

        if check_password(
            password=login_data.password, hashed_password=creds_from_storage["password"]
        ): 

            access_token, refresh_token = JWT_SERVICE.generate_tokens(
                user_id=creds_from_storage["id"],
            )
            REF_TOK_STORAGE.add_token(
                token=refresh_token,
                agent=agent,
                user_id=creds_from_storage["id"]
            )

            user_login_history_table.create(
                data={
                    "user_id": creds_from_storage["id"],
                    "user_agent": agent,
                    "refresh_token": refresh_token,
                }
            )

            return AuthRespView(access_token=access_token, refresh_token=refresh_token)
        else:
            raise AccessDenied

    @staticmethod
    def logout(access_token: str, agent: str):
        payload = JWT_SERVICE.get_access_payload(access_token)
        if payload is not None:
            REVOKED_ACCESS.add(access_token)
            REF_TOK_STORAGE.revoke_token(user_id=payload.user_id, agent=agent)
        else:
            raise InvalidToken
    
    @staticmethod
    def logout_all(access_token: str, user_id: Optional[uuid.UUID] = None):
        payload = JWT_SERVICE.get_access_payload(access_token)
        
        if payload is not None:
            if user_id is None:
                user_id = payload.user_id
            LOG_OUT_ALL.add(user_id=user_id)
        else:
            raise AccessDenied

    def authorize(self, access_token: str) -> List[str]:
        if not self.check_access_token(access_token):
            raise InvalidToken

        payload = JWT_SERVICE.get_access_payload(access_token)
        if payload is not None:
            return payload.roles
        raise InvalidToken

    @staticmethod
    def check_access_token(access_token):
        if REVOKED_ACCESS.is_ok(access_token) and LOG_OUT_ALL.is_ok(access_token) and ROLES_UPDATE.is_ok(access_token):
            return True
        else:
            return False

    @staticmethod
    def refresh_jwt(refresh_jwt: str, agent: str) -> AuthRespView:
        refresh_payload = JWT_SERVICE.get_refresh_payload(refresh_jwt)
        if (refresh_payload is None) or (not LOG_OUT_ALL.is_ok(refresh_jwt)):
            raise InvalidToken
        if refresh_jwt != REF_TOK_STORAGE.get_token(
            user_id=refresh_payload.user_id,
            agent=agent
            ):
            print("gonna check acces in storage", flush=True)
            print(REF_TOK_STORAGE.get_token(
            user_id=refresh_payload.user_id,
            agent=agent
            ), flush=True)
            raise InvalidToken
        print("check access in storage", flush=True)

        access_payload, refresh_payload = JWT_SERVICE.refresh_payloads(
            refresh_payload,
            soft=ROLES_UPDATE.is_ok(refresh_jwt)
        )

        refresh_token = JWT_SERVICE.encode(refresh_payload)
        access_token=JWT_SERVICE.encode(access_payload)

        REF_TOK_STORAGE.add_token(
            token=refresh_token,
            agent=agent,
            user_id=refresh_payload.user_id
        )
        return AuthRespView(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def token_required(self, check_is_me=False, check_is_superuser=False):
        """
        Декоратор для проверки токена. При включенном флаге check_is_me в именнованых аргументах
        функции обязательно должен быть user_id
        """
        def inner(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                access_token = request.headers.get("Authorization")
                if not access_token:
                    raise InvalidToken
                if not self.check_access_token(access_token):
                    raise InvalidToken

                payload = JWT_SERVICE.get_access_payload(access_token)
                if not payload.is_superuser and check_is_me:
                    if str(payload.user_id) != kwargs["user_id"]:
                        raise AccessDenied
                if check_is_superuser:
                    if not payload.is_superuser:
                        raise AccessDenied
                value = func(*args, **kwargs)
                return value
            return wrapper
        return inner


AUTH_SERVICE = AuthService()
