from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends

from api.v1.exceptions import NotFoundException
from api.v1.models.response_model import PersonDetailResponse, PersonPageResponse, FilmPageResponse, ListResponseFilm
from api.v1.utils import PersonQueryParams, FilmByPersonQueryParams
from services.films import FilmService, get_film_service
from services.persons import PersonService, get_person_service

router = APIRouter()


@router.get('/{person_id}', response_model=PersonDetailResponse, summary="Детали персоны")
async def person_details(
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
) -> PersonDetailResponse:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise NotFoundException
    return PersonDetailResponse(**dict(person))


@router.get('/search/', response_model=PersonPageResponse, summary="Поиск по имени")
async def search_persons_list(
        params: PersonQueryParams = Depends(),
        person_service: PersonService = Depends(get_person_service),
        page_size: int = 10,
        ) -> PersonPageResponse:
    persons: Optional[dict] = await person_service.get_many(
        sorting=params.sort,
        page_size=page_size,
        query=params.query
    )
    if not persons:
        raise NotFoundException

    persons_response_list = [PersonDetailResponse(**dict(person)) for person in persons]
    return PersonPageResponse(
        page_size=page_size,
        persons=persons_response_list
    )


@router.get('/{person_id}/film/', response_model=FilmPageResponse, summary="Фильмы по персоне")
async def get_films_by_person(
        person_id: UUID,
        params: FilmByPersonQueryParams = Depends(),
        film_service: FilmService = Depends(get_film_service),
        page_size: int = 10,
        ) -> FilmPageResponse:
    films: Optional[list] = await film_service.get_films_by_person_id(
        person_id=person_id,
        sorting=params.sort,
        page_size=page_size
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
