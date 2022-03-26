from typing import List, Optional
from uuid import UUID

from fastapi_solution.src.models.mixin import CommonMixin


class Person(CommonMixin):
    full_name: str
    roles: Optional[List[str]] = []
    film_ids: List[UUID] = []
