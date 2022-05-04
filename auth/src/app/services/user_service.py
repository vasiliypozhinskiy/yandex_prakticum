from typing import Optional
import uuid

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, DataError

from app.core import db
from app.services.storage.storage import user_table
from app.models.db_models import User as DBUserModel, UserData as DBUserDataModel, LoginHistory as DBUserLoginModel
from app.models.service_models import User as UserServiceModel, HistoryEntry as HistoryEntryServiceModel
from app.utils.exceptions import (
    AlreadyExistsError,
    BadIdFormat,
    FieldValidationError,
    NotFoundError,
    AccessDenied,
)
from app.utils.utils import hash_password, row2dict, check_password


class UserService:
    def create_user(self, user_data: dict) -> uuid:
        self.validate_user(user_data)
        user_data["password"] = hash_password(user_data["password"]).decode()

        user_id = user_table.create(data=user_data)
        # user = DBUserModel(
        #     id=user_id,
        #     login=user_data["login"],
        #     password=user_data["password"],
        #     email=user_data["email"]
        # )

        db_user_data = DBUserDataModel(
            user_id=user_id,
            birthdate=user_data.get("birthdate"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name")
        )
        
        # db.session.add(user)
        db.session.add(db_user_data)

        try:
            db.session.commit()
        except IntegrityError:
            raise AlreadyExistsError

        return user_id

    def get_user(self, user_id) -> Optional[UserServiceModel]:
        user = self.try_get_from_db(user_id)
        user_model = UserServiceModel(**user)

        return user_model

    def update_user(self, user_id, user_data) -> None:
        user = self.try_get_from_db(user_id)

        new_data = dict(user, **user_data)
        self.validate_user(new_data)

        user_base_fields = row2dict(DBUserModel).keys()
        user_data_fields = row2dict(DBUserDataModel).keys()

        try:
            DBUserModel.query.filter_by(id=user_id).update({
                key: user_data[key] for key in user_base_fields if user_data.get(key)
            })
            DBUserDataModel.query.filter_by(user_id=user_id).update({
                key: user_data[key] for key in user_data_fields if user_data.get(key)
            })
            db.session.commit()
        except IntegrityError:
            raise AlreadyExistsError

    def delete_user(self, user_id) -> None:
        self.try_get_from_db(user_id)
        DBUserModel.query.filter_by(id=user_id).delete()
        DBUserDataModel.query.filter_by(user_id=user_id).delete()
        DBUserLoginModel.query.filter_by(user_id=user_id).delete()
        db.session.commit()

    def change_password(self, user_id, passwords) -> None:
        user = self.try_get_from_db(user_id)

        if not check_password(passwords["old_password"], user["password"]):
            raise AccessDenied("Wrong password")

        user["password"] = passwords["new_password"]
        self.validate_user(user)

        user["password"] = hash_password(passwords["new_password"]).decode()

        DBUserModel.query.filter_by(id=user_id).update({"password": user["password"]})
        db.session.commit()

    def get_history(self, user_id):
        user = DBUserModel.query.filter_by(id=user_id).first()
        history = [HistoryEntryServiceModel(**row2dict(row)) for row in user.history_entries]

        return history

    @staticmethod
    def validate_user(user_data):
        try:
            UserServiceModel(**user_data)
        except ValidationError as e:
            raise FieldValidationError(message=e.__repr__())

    @staticmethod
    def try_get_from_db(id_) -> dict:
        try:
            user = DBUserModel.query.filter_by(id=id_).first()
        except DataError:
            raise BadIdFormat

        if not user:
            raise NotFoundError

        user_data = DBUserDataModel.query.filter_by(user_id=user.id).first()

        user_dict = row2dict(user_data)
        user_dict.update(row2dict(user))
        return user_dict


user_service = UserService()
