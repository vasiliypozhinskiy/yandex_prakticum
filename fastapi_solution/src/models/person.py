from typing import List, Optional
from uuid import UUID
from models.base import BaseServiceModel


class Person(BaseServiceModel):
    full_name: str
    roles: Optional[List[str]] = []
    films_ids: List[UUID] = []
