from http import HTTPStatus
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from api.v1.response_model import Film, FilmPage
from api.v1.utils import FilmQueryParams
from services.films import FilmService, get_film_service

router = APIRouter()

MESSAGE_DATA_NOT_FOUND = 'data not found'

@router.get('/{film_id}', response_model=Film, summary="Детали фильма")
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=MESSAGE_DATA_NOT_FOUND)
    return film


@router.get('/', response_model=FilmPage, summary="Поиск по жанру и названию")
async def search_film_list(
        params: FilmQueryParams = Depends(),
        film_service: FilmService = Depends(get_film_service),
        page_size: int = 10,
        ) -> FilmPage:
    films: Optional[dict] = await film_service.get_all_films(
        sorting=params.sort,
        page_size=page_size,
        query=params.query,
        genre=params.genre_filter,
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=MESSAGE_DATA_NOT_FOUND)
    return FilmPage(**films)
