from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from models.mixin import CommonMixin


class Person(CommonMixin):
    full_name: str
    roles: Optional[List[str]] = []
    films_ids: List[UUID] = []


class PersonPage(BaseModel):
    page_size: int
    persons: List[Person] = []
