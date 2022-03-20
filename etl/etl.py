import os
import time
from typing import List, Optional, Set, Tuple

import psycopg2
from psycopg2.extras import RealDictCursor, RealDictRow
from psycopg2 import OperationalError as PostgresOperationalError
from elasticsearch import Elasticsearch, RequestError
from elasticsearch.helpers import bulk
from elastic_transport import ConnectionError as ElasticConnectionError

from schema import Schema
from storage import State, JsonFileStorage
from models import ESModel, Writer, Actor
from backoff import backoff
from logger import logger


class ElasticUpdater:
    ERRORS: Tuple[Exception] = (ElasticConnectionError,)

    def __init__(self, host: str, auth: tuple):
        self.host = host
        self.auth = auth

    def get_connection(self):
        return Elasticsearch(
            hosts=[self.host],
            http_auth=(self.auth),
        )

    @backoff(errors=ERRORS)
    def create_schema(self):
        connection = self.get_connection()
        try:
            logger.info('Try to create schema')
            connection.indices.create(
                index="movies",
                body={"settings": Schema.settings, "mappings": Schema.mappings},
            )
        except RequestError as e:
            if e.status_code == 400:
                logger.info('schema already exists')
            else:
                raise e
        finally:
            connection.close()

    @backoff(errors=ERRORS)
    def load(self, data: List[ESModel]) -> None:
        def generate_docs(data):
            for item in data:
                yield {
                    '_index': 'movies',
                    '_id': item.id,
                    '_source': item.dict()
                }

        connection = self.get_connection()
        try:
            bulk(connection, generate_docs(data))
        finally:
            connection.close()


class PostgresLoader:
    ERRORS: Tuple[Exception] = (PostgresOperationalError,)
    CHUNK_SIZE: int = 100

    def __init__(self, dsl: dict, state: State):
        self.dsl = dsl
        self.connection = None
        self.state = state

    @backoff(errors=ERRORS)
    def connect(self) -> None:
        self.connection = psycopg2.connect(**dsl)

    @backoff(errors=ERRORS)
    def load_data(self, cursor: RealDictCursor, table_name: str, since_ts: str) -> List[RealDictRow]:
        modified_ids = self.get_modified_ids(cursor, table_name, since_ts)

        if table_name != 'film_work':
            modified_filmwork_ids = self.get_modified_filmworks_ids(cursor, table_name, modified_ids)
            filmwork_ids = modified_filmwork_ids if modified_filmwork_ids else []
        else:
            filmwork_ids = modified_ids

        return self.get_modified_filmworks(cursor, set(filmwork_ids))

    @backoff(errors=ERRORS)
    def get_modified_ids(self, cursor: RealDictCursor, table_name: str, since_ts: str) -> Optional[List[str]]:
        sql = f"""
            SELECT 
                id,
                modified
            FROM content.{table_name} """
        if since_ts:
            sql += f"WHERE modified > '{since_ts}'"

        sql += f"""
            ORDER BY modified, id
            LIMIT {self.CHUNK_SIZE}
            """

        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
        except Exception as e:
            logger.exception('Error while reading from Postgres')
            raise Exception

        if rows:
            self.state.set_state('temp_last_update', str(rows[-1]['modified']))

        updated_rows_count = len(rows) + self.state.get_state(table_name)
        self.state.set_state(table_name, updated_rows_count)
        return [row['id'] for row in rows]

    @backoff(errors=ERRORS)
    def get_modified_filmworks_ids(self, cursor: RealDictCursor, table_name: str, updated_ids: List[str]) -> Optional[List[str]]:
        if not updated_ids:
            return

        sql = f"""
            SELECT fw.id
            FROM content.film_work fw
            LEFT JOIN content.{table_name}_film_work pfw ON pfw.film_work_id = fw.id
            WHERE pfw.{table_name}_id IN ({str(updated_ids)[1:-1]})
            ORDER BY fw.modified, fw.id
            """

        cursor.execute(sql)
        rows = cursor.fetchall()

        return [row['id'] for row in rows]

    @backoff(errors=ERRORS)
    def get_modified_filmworks(self, cursor: RealDictCursor, updated_ids: Set[str]) -> Optional[List[RealDictRow]]:
        """
        Возвращает список строк
        """
        if not updated_ids:
            return

        sql = f"""
        SELECT
            fw.id as fw_id, 
            fw.title, 
            fw.description, 
            fw.rating, 
            fw.type, 
            fw.created, 
            fw.modified, 
            fwp.persons,
            fwg.genres
        FROM content.film_work fw
        LEFT JOIN LATERAL (
            SELECT 
                pfw.film_work_id,
                ARRAY_AGG (JSONB_BUILD_OBJECT (
                    'id', p.id,
                    'full_name', p.full_name,
                    'role', pfw.role
                    )
                ) AS persons    
            FROM content.person_film_work pfw
            JOIN content.person p ON p.id = pfw.person_id
            WHERE pfw.film_work_id = fw.id
            GROUP BY pfw.film_work_id
            ) fwp ON 1=1
        LEFT JOIN LATERAL (
            SELECT
                gfw.film_work_id,
                ARRAY_AGG (g.name) AS genres   
            FROM content.genre_film_work gfw
            JOIN content.genre g ON g.id = gfw.genre_id
            WHERE gfw.film_work_id = fw.id
            GROUP BY gfw.film_work_id
            ) fwg ON 1=1
        WHERE fw.id IN ({str(updated_ids)[1:-1]})
        """

        cursor.execute(sql)
        rows = cursor.fetchall()

        return rows


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
        self.state.set_state('temp_last_update', 0)

        while True:
            last_update = self.state.get_state(f'last_update_{table_name}')
            self.postgres_loader.connect()
            with self.postgres_loader.connection as connection:
                with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    data_chunk = self.postgres_loader.load_data(cursor, table_name, last_update)

            if not data_chunk:
                break

            serialized_data = self.serialize_data(data_chunk)
            self.elastic_updater.load(serialized_data)

            last_update: str = self.state.get_state('temp_last_update')
            self.state.set_state(f'last_update_{table_name}', last_update)

    @staticmethod
    def serialize_data(data: List[RealDictRow]) -> List[ESModel]:
        """
        Преобразуем строки из postgres в модель для elastic search.
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

            serialized_films.append(ESModel(**serialized_film))

        return serialized_films


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
    elastic_updater.create_schema()

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

