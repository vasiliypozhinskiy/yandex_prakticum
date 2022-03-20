from typing import Tuple, List

from elasticsearch import Elasticsearch, RequestError
from elasticsearch.helpers import bulk
from elastic_transport import ConnectionError as ElasticConnectionError

from es_schema.movies import Movies
from es_schema.settings import settings as schema_settings
from models import ESFilm
from utils.backoff import backoff
from utils.logger import logger


class ElasticUpdater:
    ERRORS: Tuple[Exception] = (ElasticConnectionError,)
    SCHEMAS = {
        'movies': Movies.mappings,
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

    @backoff(errors=ERRORS)
    def load(self, data: List[ESFilm]) -> None:
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
