import os
import time
from typing import List

from psycopg2.extras import RealDictCursor, RealDictRow
from pydantic import ValidationError

from storage import State, JsonFileStorage
from models import ESFilm, Writer, Actor, ESGenre
from utils.logger import logger
from elastic_updater import ElasticUpdater
from postgres_loader import PostgresLoader


class ETL:
    """
    Сервис для синхронизации данных в postgres и elastic search
    """
    SLEEP_TIME: int = 3
    TABLES_FOR_CHECK: List[str] = ['person', 'genre', 'film_work']

    def __init__(self, postgres_loader: PostgresLoader, elastic_updater: ElasticUpdater, state: State):
        self.elastic_updater = elastic_updater
        self.postgres_loader = postgres_loader
        self.state = state

    def run(self) -> None:
        while True:
            for table in self.TABLES_FOR_CHECK:
                self.load_in_elastic(table)
                logger.info(f'Check table {table}. {etl.state.get_state(table)} row updated')
            time.sleep(self.SLEEP_TIME)

    def load_in_elastic(self, table_name: str) -> None:
        """
        Метод проверки обновления данных в таблице с именем table_name в postgres и загрузки обновлённых строк в elastic search.
        """
        self.state.set_state(table_name, 0)
        self.state.set_state(f'temp_last_update_{table_name}', 0)

        while True:
            last_update = self.state.get_state(f'last_update_{table_name}')
            self.postgres_loader.connect()
            with self.postgres_loader.connection as connection:
                with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    data_chunk = self.postgres_loader.load_data(cursor, table_name, last_update)

            has_data = False
            for table_data in data_chunk.values():
                if table_data:
                    has_data = True
                    break

            if not has_data:
                break

            serialized_data = {
                'movies': self.serialize_films(data_chunk.get('movies')),
                'genres': self.serialize_genres(data_chunk.get('genres'))
            }

            self.elastic_updater.load(serialized_data)

            last_update: str = self.state.get_state(f'temp_last_update_{table_name}')
            self.state.set_state(f'last_update_{table_name}', last_update)

    @staticmethod
    def serialize_films(data: List[RealDictRow]) -> List[ESFilm]:
        """
        Преобразуем строки c фильмами из postgres в модель для elastic search.
        """
        serialized_films = []
        for film in data:
            serialized_film = {
                        "id": film["fw_id"],
                        "imdb_rating": film.get("rating"),
                        "genre": ','.join(film.get("genres")),
                        "title": film.get("title"),
                        "description": film.get("description"),
                        "director": [],
                        "actors_names": [],
                        "actors": [],
                        "writers_names": [],
                        "writers": [],
                    }

            persons = film.get('persons')
            if persons:
                for person in persons:
                    if person["role"] == "director":
                        serialized_film["director"] = [person["full_name"]]
                    if person["role"] == "writer":
                        serialized_film["writers"].append(Writer(id=person["id"], name=person["full_name"]))
                        serialized_film["writers_names"].append(person["full_name"])
                    if person["role"] == "actor":
                        serialized_film["actors"].append(Actor(id=person["id"], name=person["full_name"]))
                        serialized_film["actors_names"].append(person["full_name"])

            serialized_films.append(ESFilm(**serialized_film))

        return serialized_films

    @staticmethod
    def serialize_genres(data: List[RealDictRow]) -> List[ESGenre]:
        """
        Преобразуем строки c жанрами из postgres в модель для elastic search.
        """
        serialized_genres = []
        for genre in data:
            serialized_genre = {
                'id': genre['g_id'],
                'name': genre['name'],
                'description': genre.get('description'),
                'films_ids': genre.get('films_ids')
            }

            try:
                serialized_genres.append(ESGenre(**serialized_genre))
            except ValidationError:
                logger.error(f'Неправильные данные в postgres. {serialized_genre}')

        return serialized_genres


if __name__ == "__main__":
    storage = JsonFileStorage('/app/state/state.json')
    state = State(storage)
    elastic_updater = ElasticUpdater(
        host=os.environ.get('ELASTIC_HOST'),
        auth=(
            os.environ.get('ELASTIC_USER'),
            os.environ.get('ELASTIC_PASSWORD')
        )
    )

    elastic_updater.create_schemas()

    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT')
    }

    postgres_loader = PostgresLoader(dsl, state)

    etl = ETL(postgres_loader=postgres_loader, elastic_updater=elastic_updater, state=state)

    etl.run()

