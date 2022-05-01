from typing import Optional, List
from uuid import UUID

from pydantic.main import BaseModel

class AuthReqView(BaseModel):
    login: str
    password: str

class AuthRespView(BaseModel):
    access_token: str
    refresh_token: str

class AuthRefreshReqView(BaseModel):
    refresh_token: str

class AuthRefreshRespView(BaseModel):
    access_token: str
    refresh_token: str
    