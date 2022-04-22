from sqlalchemy.exc import IntegrityError

from app.models.db_models import User as DBUserModel
from app.models.service_models import User as UserServiceModel
from app.core import db
from app.utils.exceptions import ValidationError, AlreadyExistsError, BadPasswordError, BadEmailError
from app.utils.utils import hash_password


class UserService:
    def create_user(self, **kwargs):
        try:
            self.validate_user(**kwargs)
            kwargs['password'] = hash_password(kwargs['password']).decode()
            user = DBUserModel(**kwargs)
        except BadPasswordError as e:
            raise e
        except BadEmailError as e:
            raise e
        except TypeError:
            raise ValidationError
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            raise AlreadyExistsError

    @staticmethod
    def get_user(user_id) -> UserServiceModel:
        try:
            user = DBUserModel.query.filter_by(id=user_id).first()
            user_model = UserServiceModel(**user.__dict__)
        except Exception as e:
            raise e

        return user_model

    @staticmethod
    def validate_user(**kwargs):
        user = UserServiceModel(**kwargs)




