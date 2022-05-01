from app.core import db
from app.models.db_models import Role
from app.utils.exceptions import AlreadyExistsError
from app.utils.exceptions import BadIdFormat, NotFoundError
from sqlalchemy.exc import IntegrityError, DataError


class RoleService:
    @staticmethod
    def create_role(role: str) -> None:
        role = Role(title=role)
        db.session.add(role)
        try:
            db.session.commit()
        except IntegrityError:
            raise AlreadyExistsError

    def delete_role(self, role_title) -> None:
        self.try_get_from_db(role_title)
        Role.query.filter_by(title=role_title).delete()
        db.session.commit()

    @staticmethod
    def get_list_role():
        roles = {}
        role = [x.title for x in Role.query.all()]
        roles["role_list"] = role
        return roles

    def update_role(self, role_title, new_role):
        role = Role.query.filter_by(title=role_title).first()
        if not role:
            raise NotFoundError("Role not found")

        roles = self.get_list_role()
        if new_role in roles["role_list"]:
            raise AlreadyExistsError("Role already exists")

        Role.query.filter_by(title=role_title).update({"title": new_role})
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
