import uuid
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime, timedelta
from typing import Optional, Tuple

from pydantic import BaseModel
import jwt
from jwt.exceptions import DecodeError, InvalidSignatureError

from app.models.db_models import User
from app.utils.exceptions import InvalidToken, AccessDenied
from app.core.config import SECRET_SIGNATURE, REFRESH_TOKEN_EXP, ACCESS_TOKEN_EXP


class BasePayload(BaseModel):
    iat: int
    exp: int
    user_id: uuid.UUID


class RefreshPayload(BasePayload):
    pass


class AccessPayload(BasePayload):
    roles: List[str]
    is_superuser: bool


class BaseServiceJWT(ABC):

    @abstractmethod
    def generate_tokens(self, user_id) -> Tuple[str, str]:
        pass

    @abstractmethod
    def get_access_payload(self, token) -> AccessPayload:
        pass
    
    @abstractmethod
    def get_refresh_payload(self, token) -> RefreshPayload:
        pass


class ServiceJWT(BaseServiceJWT):

    def __init__(self, access_timeout: int, refresh_timeout: int):
        self.access_timeout = access_timeout
        self.refresh_timeout = refresh_timeout
    
    def generate_tokens(self, user_id) -> Tuple[str, str]:
        return (
            self._get_access_jwt(user_id),
            self._get_refresh_jwt(user_id)
        )

    def get_access_payload(self, token) -> Optional[AccessPayload]:
        payload = self.decode_token(token)
        return AccessPayload(**payload) if payload else None
    
    def get_refresh_payload(self, token) -> Optional[RefreshPayload]:
        payload = self.decode_token(token)
        return RefreshPayload(**payload) if payload else None

    @staticmethod
    def decode_token(token) -> Optional[dict]:
        try:
            payload = jwt.decode(token, SECRET_SIGNATURE, algorithms=["HS256"])
        except (
            DecodeError,
            InvalidSignatureError,
        ):
            raise InvalidToken
        return payload
        
    def _get_refresh_jwt(self, user_id: uuid.UUID):
        #TODO Отдавать рефреш токен
        return self._get_access_jwt(user_id=user_id)

    def _get_access_jwt(self, user_id: uuid.UUID) -> str:
        user = User.query.filter_by(id=user_id).first()

        payload = {
            "exp": datetime.now() + timedelta(seconds=self.access_timeout),
            "iat": datetime.now(),
            "user_id": str(user_id),
            "roles": user.roles,
            "is_superuser": user.is_superuser
        }
        return jwt.encode(
            payload,
            SECRET_SIGNATURE,
            algorithm="HS256",
        )


JWT_SERVICE = ServiceJWT(refresh_timeout=REFRESH_TOKEN_EXP, access_timeout=ACCESS_TOKEN_EXP)