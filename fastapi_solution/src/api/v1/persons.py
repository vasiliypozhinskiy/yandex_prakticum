from http import HTTPStatus

from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.v1.utils import PersonQueryParams, FilmByPersonQueryParams
from services.persons import PersonService, get_person_service
from models.person import PersonPage
from models.film import FilmsByPerson

router = APIRouter()


class Person(BaseModel):
    """полная информация по персоне"""
    id: UUID
    full_name: str
    films_ids: List[UUID]


@router.get('/{person_id}', response_model=Person, summary="Детали персоны")
async def person_details(person_id: UUID, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person


@router.get('/search/', response_model=PersonPage, summary="Поиск по имени")
async def search_persons_list(
        params: PersonQueryParams = Depends(),
        person_service: PersonService = Depends(get_person_service),
        page_size: int = 10,
        ) -> PersonPage:
    persons: Optional[dict] = await person_service.get_all_persons(
        sorting=params.sort,
        page_size=page_size,
        query=params.query
    )
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return PersonPage(**persons)


@router.get('/{person_id}/film/', response_model=FilmsByPerson, summary="Фильмы по персоне")
async def get_films_by_person(
        person_id: UUID,
        params: FilmByPersonQueryParams = Depends(),
        person_service: PersonService = Depends(get_person_service),
        page_size: int = 10,
        ) -> FilmsByPerson:
    films: Optional[dict] = await person_service.get_films_by_person(
        person_id=person_id,
        sorting=params.sort,
        page_size=page_size
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')
    return FilmsByPerson(**films)
