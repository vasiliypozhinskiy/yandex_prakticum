from typing import Optional

from pydantic.main import BaseModel


class UserResponse(BaseModel):
    login: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    birthdate: Optional[str]

