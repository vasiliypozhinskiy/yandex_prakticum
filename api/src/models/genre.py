from typing import Optional, List
from uuid import UUID
from models.base import BaseServiceModel


class Genre(BaseServiceModel):
    name: str
    description: Optional[str]
    films_ids: Optional[List[UUID]]
