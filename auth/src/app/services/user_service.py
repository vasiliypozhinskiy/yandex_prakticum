from typing import Optional

from app.core import db
from app.models.db_models import User as DBUserModel
from app.models.service_models import User as UserServiceModel
from app.utils.exceptions import AlreadyExistsError, BadIdFormat, FieldValidationError, NotFoundError
from app.utils.utils import hash_password, row2dict
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, DataError


class UserService:
    def create_user(self, user_data: dict) -> None:
        self.validate_user(user_data)
        user_data['password'] = hash_password(user_data['password']).decode()
        user = DBUserModel(**user_data)

        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError:
            raise AlreadyExistsError

    def get_user(self, user_id) -> Optional[UserServiceModel]:
        user = self.try_get_from_db(user_id)
        user_model = UserServiceModel(**row2dict(user))

        return user_model

    def update_user(self, user_id, user_data) -> None:
        user = self.try_get_from_db(user_id)

        old_data = row2dict(user)
        new_data = dict(old_data, **user_data)

        self.validate_user(new_data)

        try:
            DBUserModel.query.filter_by(id=user_id).update(user_data)
            db.session.commit()
        except IntegrityError:
            raise AlreadyExistsError

    def delete_user(self, user_id) -> None:
        print(user_id)
        self.try_get_from_db(user_id)

        DBUserModel.query.filter_by(id=user_id).delete()
        db.session.commit()

    @staticmethod
    def validate_user(user_data):
        try:
            UserServiceModel(**user_data)
        except ValidationError as e:
            raise FieldValidationError(message=e.__repr__())

    @staticmethod
    def try_get_from_db(id_):
        try:
            user = DBUserModel.query.filter_by(id=id_).first()
        except DataError:
            raise BadIdFormat

        if not user:
            raise NotFoundError

        return user





