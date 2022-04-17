from abc import ABC, abstractmethod


class AbstractDB(ABC):

    @abstractmethod
    def get_by_id(self, index, id_):
        pass

    @abstractmethod
    def search(self, index, params):
        pass

    @abstractmethod
    def close(self):
        pass


db: AbstractDB

async def get_db() -> AbstractDB:
    return db
