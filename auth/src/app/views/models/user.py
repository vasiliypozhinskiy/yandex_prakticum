from typing import Optional, List
from uuid import UUID

from pydantic.main import BaseModel


class UserResponse(BaseModel):
    login: str
    email: str
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]

