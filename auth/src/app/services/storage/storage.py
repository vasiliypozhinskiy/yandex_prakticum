from abc import ABC, abstractmethod
import uuid

from app.core import db
from app.models.db_models import User
from app.utils.exceptions import (
    AlreadyExistsError,
    BadIdFormat,
    NotFoundError,
)
from app.utils.utils import row2dict

from sqlalchemy.exc import IntegrityError, DataError

class BaseTable(ABC):
    
    @abstractmethod
    def create(self, object):
        pass

    @abstractmethod
    def read(self, id):
        pass

    @abstractmethod
    def update(self, user_id):
        pass

    @abstractmethod
    def delete(self, id):
        pass


class SQLAlchemyTable(BaseTable):

    def __init__(self, model: db.Model, id_field: str = "id"):
        self.model = model
        self.id_field = id_field
        self.mode_keys = row2dict(self.model).keys()

    def create(self, data) -> uuid.UUID:
        new_id = uuid.uuid4()

        new_object = self.model(**self._filter_input_to_model(data))

        db.session.add(new_object)

        try:
            db.session.commit()
        except IntegrityError:
            raise AlreadyExistsError

        return new_id

    def read(self, id) -> dict:
        obj_as_dict = self._try_get_from_db(id)
        return obj_as_dict

    def update(self, id, data):
        _ = self._try_get_from_db(id)
        try:
            self.model.query.filter_by(id=id).update(
                self._filter_input_to_model(data)
            )
            db.session.commit()
        except IntegrityError:
            raise AlreadyExistsError

    def delete(self, id) -> None:
        self.try_get_from_db(id)
        db.session.commit()

    def _filter_input_to_model(self, data: dict) -> dict:
        return {
            key: data[key] for key in self.mode_keys if data.get(key)
        }

    def _try_get_from_db(self, id_) -> dict:
        try:
            obj = self.model.query.filter_by(**{"self.id_field": id_}).first()
        except DataError:
            raise BadIdFormat

        if not obj:
            raise NotFoundError
        user_dict = row2dict(obj)
        return user_dict

user_table = SQLAlchemyTable(User)