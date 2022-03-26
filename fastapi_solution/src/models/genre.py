from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from models.mixin import CommonMixin


class Genre(CommonMixin):
    name: str
    description: Optional[str] = None
    films_ids: Optional[List[UUID]] = None


class GenrePage(BaseModel):
    page_size: int
    genres: List[Genre] = []
