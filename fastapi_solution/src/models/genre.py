from typing import Optional, List

from fastapi_solution.src.models.mixin import CommonMixin


class Genre(CommonMixin):
    name: str
    description: Optional[str] = None
    film_ids: Optional[List[str]] = None