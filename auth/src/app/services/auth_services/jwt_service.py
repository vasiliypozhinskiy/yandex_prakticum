import uuid

from abc import ABC, abstractmethod
from typing import Tuple, List
from pydantic import BaseModel

from datetime import datetime, timedelta
from typing import Optional, Tuple

from app.utils.exceptions import InvalidToken
from app.core.config import SECRET_SIGNATURE, REFRESH_TOKEN_EXP, ACCESS_TOKEN_EXP

import jwt
from jwt.exceptions import DecodeError, InvalidSignatureError

class RefreshPayload(BaseModel):
    iat: int
    exp: int
    user_id: uuid.UUID

class AccessPayload(RefreshPayload):
    roles: List[str]


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
        payload = self._validate_token(token)
        return AccessPayload(**payload) if payload is not None else None
    
    def get_refresh_payload(self, token) -> Optional[RefreshPayload]:
        payload = self._validate_token(token)
        return RefreshPayload(**payload) if payload is not None else None


    def _validate_token(self, token) -> Optional[dict]:
        try:
            payload = jwt.decode(token, SECRET_SIGNATURE, algorithms=["HS256"])
        except (
            DecodeError,
            InvalidSignatureError,
        ):
            raise InvalidToken
        return payload
        
    def _get_refresh_jwt(self, user_id: uuid.UUID):
        return self._get_access_jwt(user_id=user_id)

    def _get_access_jwt(self, user_id: uuid.UUID) -> str:

        roles = ['None']
        payload = {
            "exp": datetime.now() + timedelta(seconds=self.access_timeout),
            "iat": datetime.now(),
            "user_id": str(user_id),
            "roles": roles,
        }
        return jwt.encode(
            payload,
            SECRET_SIGNATURE,
            algorithm="HS256",
        )


JWT_SERVICE = ServiceJWT(refresh_timeout=REFRESH_TOKEN_EXP, access_timeout=ACCESS_TOKEN_EXP)