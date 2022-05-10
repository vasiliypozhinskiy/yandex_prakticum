from typing import Optional

from fastapi import APIRouter, Depends, Header

from api.v1.exceptions import NotFoundException, ComedySubscription
from api.v1.models.response_model import FilmDetailResponse, FilmPageResponse, ListResponseFilm
from api.v1.utils import FilmQueryParams
from services.films import FilmService, get_film_service
from services.auth import is_superuser

router = APIRouter()


@router.get('/{film_id}', response_model=FilmDetailResponse, summary="Детали фильма")
async def film_details(
        film_id: str,
        film_service: FilmService = Depends(get_film_service),
        authorize: Optional[str] = Header(None),
) -> FilmDetailResponse:
    film = await film_service.get_by_id(film_id)
    is_su = is_superuser(authorize)
    if not film:
        raise NotFoundException
    if (film.genre is not None) and ('Comedy' in film.genre):
        if not is_su:
            raise ComedySubscription
            

    return FilmDetailResponse(**dict(film))


@router.get('/search/', response_model=FilmPageResponse, summary="Поиск по жанру и названию")
async def search_film_list(
        params: FilmQueryParams = Depends(),
        film_service: FilmService = Depends(get_film_service),
        page_size: int = 10,
    ) -> FilmPageResponse:
    films = await film_service.get_many(
        sorting=params.sort,
        page_size=page_size,
        query=params.query,
        genre=params.genre_filter,
    )
    if not films:
        raise NotFoundException

    list_response_films = [ListResponseFilm(
        id=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating
        ) for film in films
    ]

    return FilmPageResponse(
        films=list_response_films,
        page_size=page_size
    )
