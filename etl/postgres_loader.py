from typing import Tuple, List, Optional, Set

import psycopg2
from psycopg2 import OperationalError as PostgresOperationalError
from psycopg2.extras import RealDictCursor, RealDictRow

from storage import State
from utils.backoff import backoff
from utils.logger import logger


class PostgresLoader:
    ERRORS: Tuple[Exception] = (PostgresOperationalError,)
    CHUNK_SIZE: int = 500

    def __init__(self, dsl: dict, state: State):
        self.dsl = dsl
        self.connection = None
        self.state = state

    @backoff(errors=ERRORS)
    def connect(self) -> None:
        self.connection = psycopg2.connect(**self.dsl)

    @backoff(errors=ERRORS)
    def load_data(self, cursor: RealDictCursor, table_name: str, since_ts: str) -> dict:
        modified_ids = self.get_modified_ids_by_since_ts(cursor, table_name, since_ts)

        filmwork_ids = []
        genre_ids = []
        if table_name == 'film_work':
            filmwork_ids = modified_ids
            genre_ids = self.get_modified_id_by_filmwork_ids(cursor, 'genre', modified_ids)

        if table_name == 'genre':
            filmwork_ids = self.get_modified_filmworks_ids(cursor, table_name, modified_ids)
            genre_ids = modified_ids

        if table_name == 'person':
            filmwork_ids = self.get_modified_filmworks_ids(cursor, table_name, modified_ids)

        data = {
            'movies': self.get_modified_filmworks(cursor, set(filmwork_ids)),
            'genres': self.get_modified_genres(cursor, set(genre_ids))
        }

        return data

    @backoff(errors=ERRORS)
    def get_modified_ids_by_since_ts(
        self,
        cursor: RealDictCursor,
        table_name: str,
        since_ts: str
    ) -> Optional[List[str]]:
        sql = f"""
            SELECT 
                id,
                modified
            FROM content.{table_name} 
            """
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
            raise e

        if rows:
            self.state.set_state(f'temp_last_update_{table_name}', str(rows[-1]['modified']))

        updated_rows_count = len(rows) + self.state.get_state(table_name)
        self.state.set_state(table_name, updated_rows_count)
        return [row['id'] for row in rows]

    @backoff(errors=ERRORS)
    def get_modified_id_by_filmwork_ids(
            self,
            cursor: RealDictCursor,
            table_name: str,
            filmwork_ids: List[str]
    ) -> List[str]:
        if not filmwork_ids:
            return []

        sql = f"""
            SELECT {table_name}.id
            FROM content.{table_name} as {table_name}
            LEFT JOIN content.{table_name}_film_work pfw ON pfw.{table_name}_id = {table_name}.id
            WHERE pfw.film_work_id IN ({str(filmwork_ids)[1:-1]})
            ORDER BY {table_name}.modified, {table_name}.id
            """

        cursor.execute(sql)
        rows = cursor.fetchall()

        return [row['id'] for row in rows]

    @backoff(errors=ERRORS)
    def get_modified_filmworks_ids(
        self,
        cursor: RealDictCursor,
        table_name: str,
        updated_ids: List[str]
    ) -> List[str]:
        if not updated_ids:
            return []

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
    def get_modified_filmworks(self, cursor: RealDictCursor, updated_ids: Set[str]) -> List[RealDictRow]:
        """
        Возвращает список строк с изменёнными фильмами.
        """
        if not updated_ids:
            return []

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

    @backoff(errors=ERRORS)
    def get_modified_genres(self, cursor: RealDictCursor, updated_ids: Set[str]) -> Optional[List[RealDictRow]]:
        """
        Возвращает список строк с изменёнными жанрами.
        """
        if not updated_ids:
            return []

        sql = f"""
        SELECT
            g.id as g_id,
            g.name,
            g.description,
            fwg.films_ids
        FROM content.genre g
        LEFT JOIN LATERAL (
            SELECT
                g.id,
                ARRAY_AGG (fw.id::text) AS films_ids 
            FROM content.genre_film_work gfw
            JOIN content.film_work fw ON fw.id = gfw.film_work_id
            WHERE gfw.genre_id = g.id
            GROUP BY g.id
            ) fwg ON 1=1   
        WHERE g.id IN ({str(updated_ids)[1:-1]})           
        """

        cursor.execute(sql)
        return cursor.fetchall()
