from psycopg2.extensions import connection as _connection


class PostgresLoader:
    def __init__(self, connection: _connection):
        self.connection = connection

    def load_data(self):
        pass
