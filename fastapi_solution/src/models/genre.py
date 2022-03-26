from typing import Optional, List
from uuid import UUID

from fastapi_solution.src.models.mixin import CommonMixin


class Genre(CommonMixin):
    name: str
    description: Optional[str] = None
    film_ids: Optional[List[UUID]] = None