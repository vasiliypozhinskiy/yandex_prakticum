from abc import ABC, abstractmethod
import uuid
from typing import Dict, Any, Optional, List

from app.core import db
from app.models.db_models import User, UserData, LoginHistory, Role, user_role
from app.utils.exceptions import (
    AlreadyExistsError,
    BadIdFormat,
    NotFoundError,
)
from app.utils.utils import row2dict

from sqlalchemy.exc import IntegrityError, DataError


def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value), flush=True)


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


class SQLAlchemyModel(BaseTable):

    def __init__(self, model: db.Model, id_field: str = "id"):
        self.model = model
        self.id_field = id_field
        self.mode_keys = self._get_columns()

    def _get_columns(self):
        return row2dict(self.model).keys()

    def create(self, data, new_id: Optional[str] = None) -> uuid.UUID:
        if new_id is None:
            new_id = uuid.uuid4()
        data.update({self.id_field: new_id})

        new_object = self.model(**self._filter_input_to_model(data))

        db.session.add(new_object)

        try:
            db.session.commit()
        except IntegrityError:
            raise AlreadyExistsError

        return new_id

    def read(self, filter: Dict[str, Any]) -> List[dict]:
        obj_as_dict = self._try_get_from_db(filter=filter)
        return obj_as_dict

    def update(self, data, filter: Dict[str, Any]) -> None:
        _ = self._try_get_from_db(filter=filter)
        try:
            self.model.query.filter_by(**filter).update(
                self._filter_input_to_model(data)
            )
            db.session.commit()
        except IntegrityError:
            raise AlreadyExistsError

    def delete(self, filter: Optional[Dict[str, Any]] = None) -> None:
        if filter is None:
            filter = {}
        _ = self._try_get_from_db(filter)
        self.model.query.filter_by(**filter).delete()
        db.session.commit()

    def _filter_input_to_model(self, data: dict) -> dict:
        return {
            key: data[key] for key in self.mode_keys if data.get(key)
        }

    def _try_get_from_db(self, filter: Dict[str, Any]) -> dict:
        try:
            obj = self.model.query.filter_by(**filter).first()
        except DataError:
            raise BadIdFormat

        if not obj:
            raise NotFoundError
        user_dict = row2dict(obj)
        return user_dict

class UserTable(SQLAlchemyModel):

    def __init__(self, model: db.Model, roles_model: db.Model, id_field: str = "id"):
        super().__init__(model=model, id_field=id_field)
        self.roles_model = roles_model

    def add_role(self, user_id: str = None, role_title: str = None):
        user = self.model.query.filter_by(id=user_id).first()
        role = self.roles_model.query.filter_by(title=role_title).first()
        if not user or not role:
            raise NotFoundError("Role or user not found")
        list_roles_in_user = [x.title for x in user.roles]
        if role.title in list_roles_in_user:
            return AlreadyExistsError("Role already exist")
        user.roles.append(role)
        db.session.commit()

    def delete_role(self, user_id: str = None, role_title: str = None):
        user = self.model.query.filter_by(id=user_id).first()
        role = self.roles_model.query.filter_by(title=role_title).first()
        user.roles.remove(role)
        db.session.commit()


class RolesTable(SQLAlchemyModel):
    def read(self, filter: Dict[str, Any]) -> List[dict]:
        try:
            objects = self.model.query.filter_by(**filter).all()
        except DataError:
            raise BadIdFormat

        if not objects:
            return []
        roles_list = [row2dict(obj) for obj in objects]
        return roles_list

user_table = UserTable(User, roles_model=Role)
user_data_table = SQLAlchemyModel(UserData)
user_login_history_table = SQLAlchemyModel(LoginHistory)
roles_table = RolesTable(Role, id_field="title")
