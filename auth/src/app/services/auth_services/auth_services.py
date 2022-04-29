from typing import List

from app.views.models.auth import AuthReqView, AuthRespView
from app.models.db_models import User as DBUserModel
from app.utils.utils import check_password
from app.utils.exceptions import BadPasswordError, UnExistingLogin, InvalidToken
from app.services.auth_services.jwt_service import JWT_SERVICE
from app.services.auth_services.storages import REF_TOK_STORAGE
from app.services.auth_services.black_list import REVOKED_ACCESS


class AuthService:

    def login(self, request_data: AuthReqView) -> AuthRespView:
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
            return BadPasswordError, 403


    def logout(self, request):
        access_token = request.headers.get("Authorization") or ""
        
        print("access_token got", flush=True)
        payload = JWT_SERVICE.get_access_payload(access_token)
        if payload is not None:
            REVOKED_ACCESS.add(access_token)

            return 
        else:
            raise InvalidToken

    def logout_all(self, request):
        return

    def authorize(self, request) -> List[str]:
        access_token = request.headers.get("Authorization") or ""
        payload = JWT_SERVICE.get_access_payload(access_token)
        if payload is not None:
            if REVOKED_ACCESS.is_ok(access_token):
                payload.roles
        raise InvalidToken

AUTH_SERVICE = AuthService()