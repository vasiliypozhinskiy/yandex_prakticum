from app.core import db
from app.models.db_models import Role
from app.utils.exceptions import AlreadyExistsError
from app.utils.exceptions import BadIdFormat, NotFoundError,RoleAlreadyExists
from sqlalchemy.exc import IntegrityError, DataError


class RoleService:
    def create_role(self, role: dict) -> None:
        role = Role(**role)
        db.session.add(role)
        try:
            db.session.commit()
        except IntegrityError:
            raise AlreadyExistsError

    def delete_role(self, role_title) -> None:
        self.try_get_from_db(role_title)
        Role.query.filter_by(title=role_title).delete()
        db.session.commit()

    def get_list_role(self):
        roles = {}
        role = [x.title for x in Role.query.all()]
        roles['role_list'] = role
        return roles

    def update_role(self, role_title, new_role):
        role = self.try_get_from_db(role_title)
        roles = self.get_list_role()
        if new_role in roles['role_list']:
            raise RoleAlreadyExists
        Role.query.filter_by(title=role_title).update(new_role)
        db.session.commit()

    @staticmethod
    def try_get_from_db(role_title):
        try:
            role = Role.query.filter_by(title=role_title).first()
        except DataError:
            raise BadIdFormat
        if not role:
            raise NotFoundError
        return role


role_service = RoleService()
