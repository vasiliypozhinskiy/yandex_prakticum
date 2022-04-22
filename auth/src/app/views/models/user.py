from typing import Optional, List
from uuid import UUID

from pydantic.main import BaseModel


class UserResponse(BaseModel):
    id: UUID
    login: str
    is_superuser: bool
    email: str
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]

    history_entries: Optional[List[UUID]]
    roles: Optional[List[str]]
