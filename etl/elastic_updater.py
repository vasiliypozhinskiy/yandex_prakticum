from typing import Tuple, List

from elasticsearch import Elasticsearch, RequestError, ConnectionError
from elasticsearch.helpers import bulk

from es_schema.movies import Movies
from es_schema.genres import Genres
from es_schema.persons import Persons
from es_schema.settings import settings as schema_settings
from utils.backoff import backoff
from utils.logger import logger


class ElasticUpdater:
    ERRORS: Tuple[Exception] = (ConnectionError, ConnectionRefusedError)
    SCHEMAS = {
        'movies': Movies.mappings,
        'genres': Genres.mappings,
        'persons': Persons.mappings
    }

    def __init__(self, host: str, auth: tuple):
        self.host = host
        self.auth = auth

    def get_connection(self):
        return Elasticsearch(
            hosts=[self.host],
            http_auth=self.auth,
        )

    def create_schemas(self) -> None:
        for index_name, index_schema in self.SCHEMAS.items():
            self._create_schema(index_name, index_schema)

    @backoff(errors=ERRORS)
    def _create_schema(self, name: str, schema: dict) -> None:
        connection = self.get_connection()
        try:
            logger.info(f'Try to create schema {name}')
            connection.indices.create(
                index=name,
                body={"settings": schema_settings, "mappings": schema},
            )
        except RequestError as e:
            if e.status_code == 400:
                logger.info(f'schema {name} already exists')
            else:
                raise e
        finally:
            connection.close()

    def load(self, data: dict):
        for index, values in data.items():
            self._do_load(index, values)

    @backoff(errors=ERRORS)
    def _do_load(self, index: str, data: list) -> None:
        connection = self.get_connection()
        try:
            bulk(connection, self.generate_docs(index, data))
        finally:
            connection.close()

    @staticmethod
    def generate_docs(index: str, data: list):
        for item in data:
            yield {
                '_index': index,
                '_id': item.id,
                '_source': item.dict()
            }
