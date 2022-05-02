import uuid
from abc import ABC, abstractmethod
from typing import Optional, Tuple, List

from pydantic import BaseModel
import jwt
from jwt.exceptions import DecodeError, InvalidSignatureError

from app.models.db_models import User
from app.utils.exceptions import InvalidToken, AccessDenied
from app.utils.utils import get_now_ms
from app.core.config import SECRET_SIGNATURE, REFRESH_TOKEN_EXP, ACCESS_TOKEN_EXP


class BasePayload(BaseModel, ABC):
    iat: int
    exp: int
    user_id: uuid.UUID
    roles: List[str]
    is_superuser: bool


class RefreshPayload(BasePayload):
    pass


class AccessPayload(BasePayload):
    pass


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

    @staticmethod
    def encode(payload: BaseModel):
        payload = payload.dict()
        payload['user_id'] = str(payload['user_id'])
        return jwt.encode(
                payload,
                SECRET_SIGNATURE,
                algorithm="HS256",
            )
        
    def _get_refresh_jwt(self, user_id: uuid.UUID):
        user = User.query.filter_by(id=user_id).first()
        now_ms = get_now_ms()
        payload = {
            "exp": now_ms + self.refresh_timeout * 1000,
            "iat": now_ms,
            "user_id": user_id,
            "roles": user.roles,
            "is_superuser": user.is_superuser
        }
        payload = AccessPayload(**payload)
        return self.encode(payload=payload)

    def _get_access_jwt(self, user_id: uuid.UUID) -> str:
        user = User.query.filter_by(id=user_id).first()
        now_ms = get_now_ms()
        payload = {
            "exp": now_ms + self.access_timeout * 1000,
            "iat": now_ms,
            "user_id": user_id,
            "roles": user.roles,
            "is_superuser": user.is_superuser
        }
        payload = AccessPayload(**payload)
        return self.encode(payload=payload)
    
    def refresh_payloads(self, refresh: RefreshPayload, soft: bool = True) -> Tuple[AccessPayload, RefreshPayload]:
        now = get_now_ms()
        # refresh refresh
        if refresh.exp > now:
            refresh.iat = now
            refresh.exp = now + REFRESH_TOKEN_EXP
        
        # build new access
        access = AccessPayload(
            iat=now,
            exp=now + ACCESS_TOKEN_EXP,
            user_id=refresh.user_id, 
            is_superuser=refresh.is_superuser,
            roles=refresh.roles
        )

        # on special key upd roles
        if not soft:
            access.roles = self._get_roles(user_id=refresh.user_id)
            refresh.roles = self._get_roles(user_id=refresh.user_id)

        return (access, refresh)

    @staticmethod
    def _get_roles(user_id: uuid.UUID):
        user = User.query.filter_by(id=user_id).first()
        return user.roles




JWT_SERVICE = ServiceJWT(refresh_timeout=REFRESH_TOKEN_EXP, access_timeout=ACCESS_TOKEN_EXP)