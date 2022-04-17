from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends

from api.v1.exceptions import NotFoundException
from api.v1.models.response_model import GenreDetailResponse, GenrePageResponse
from api.v1.utils import GenreQueryParams
from services.genres import GenreService, get_genre_service

router = APIRouter()


@router.get('/{genre_id}', response_model=GenreDetailResponse, summary="Детали жанра")
async def genre_details(
        genre_id: str,
        genre_service: GenreService = Depends(get_genre_service)
) -> GenreDetailResponse:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise NotFoundException
    return GenreDetailResponse(**dict(genre))


@router.get('/', response_model=GenrePageResponse, summary="Список всех жанром, сортировка по названию")
async def search_genre_list(
        params: GenreQueryParams = Depends(),
        genre_service: GenreService = Depends(get_genre_service),
        page_size: int = 10,
        ) -> GenrePageResponse:
    genres: Optional[list] = await genre_service.get_many(
        sorting=params.sort,
        page_size=page_size,
    )
    if not genres:
        raise NotFoundException
    genre_response_list = [GenreDetailResponse(**dict(genre)) for genre in genres]

    return GenrePageResponse(
        page_size=page_size,
        genres=genre_response_list
    )
