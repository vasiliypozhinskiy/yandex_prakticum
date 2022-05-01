from http import HTTPStatus

from flask import request, Blueprint
from flasgger.utils import swag_from
from flask.views import MethodView

from app.models.db_models import User, Role
from app.core import db
from app.core.swagger_config import SWAGGER_DOCS_PATH
from app.services.auth_services.auth_services import AUTH_SERVICE
from app.utils.exceptions import NotFoundError, AlreadyExistsError
from app.utils.utils import check_password
from app.views.utils.decorator import catch_exceptions

user_role_blueprint = Blueprint("user_role", __name__, url_prefix="/auth/api/v1")


class UserRoleView(MethodView):
    @swag_from(
        f"{SWAGGER_DOCS_PATH}/role/add_role_for_user.yaml",
        endpoint="user_role.add_role",
    )
    @catch_exceptions
    def post(self, user_id, role_title):
        self._add_role(user_id, role_title)
        return "Роль успешно добавленна", HTTPStatus.OK

    @swag_from(
        f"{SWAGGER_DOCS_PATH}/role/remove_role_for_user.yaml",
        endpoint="user_role.delete_role",
    )
    @catch_exceptions
    def delete(self, user_id, role_title):
        self._delete_role(user_id, role_title)
        return "Роль успешно удалена", HTTPStatus.OK

    @staticmethod
    @AUTH_SERVICE.token_required(check_is_superuser=True)
    def _delete_role(user_id: str = None, role_title: str = None):
        user = User.query.filter_by(id=user_id).first()
        role = Role.query.filter_by(title=role_title).first()
        user.roles.remove(role)
        db.session.commit()

    @staticmethod
    @AUTH_SERVICE.token_required(check_is_superuser=True)
    def _add_role(user_id: str = None, role_title: str = None):
        user = User.query.filter_by(id=user_id).first()
        role = Role.query.filter_by(title=role_title).first()
        if not user or not role:
            raise NotFoundError("Role or user not found")
        list_roles_in_user = [x.title for x in user.roles]
        if role.title in list_roles_in_user:
            return AlreadyExistsError("Role already exist")
        user.roles.append(role)
        db.session.commit()


class ChangeSuperuserRights(MethodView):
    @swag_from(
        f"{SWAGGER_DOCS_PATH}/role/create_admin.yaml",
        endpoint="user_role.create_admin",
    )
    @catch_exceptions
    def post(self):
        self._create_admin()
        return "Admin created", HTTPStatus.OK

    @swag_from(
        f"{SWAGGER_DOCS_PATH}/role/delete_admin.yaml",
        endpoint="user_role.delete_admin",
    )
    @catch_exceptions
    def delete(self, user_id):
        self._delete_admin(user_id)
        return "Admin deleted", HTTPStatus.OK

    @staticmethod
    @AUTH_SERVICE.token_required(check_is_superuser=True)
    def _create_admin():
        data = request.json
        user = User.query.filter_by(email=data['email']).first()

        if not user:
            raise NotFoundError
        if user.is_superuser:
            raise AlreadyExistsError("Already admin")
        if check_password(data['password'], user.password):
            # Логика для отправки email с ссылкой для подтверждения действия
            db.session.query(User).get(user.id).is_superuser = True
            db.session.commit()

    @staticmethod
    @AUTH_SERVICE.token_required(check_is_superuser=True)
    def _delete_admin(user_id: str):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise NotFoundError("User not found")
        if not user.is_superuser:
            raise AlreadyExistsError("Already not admin")

        # Логика для отправки email с ссылкой для подтверждения действия
        db.session.query(User).get(user_id).is_superuser = False
        db.session.commit()


user_role_blueprint.add_url_rule(
    "/user_add_role/<string:user_id>/<string:role_title>",
    endpoint="add_role",
    methods=["POST"],
    view_func=UserRoleView.as_view("user_role")
)

user_role_blueprint.add_url_rule(
    "/user_delete_role/<string:user_id>/<string:role_title>",
    endpoint="delete_role",
    methods=["DELETE"],
    view_func=UserRoleView.as_view("user_role")
)

user_role_blueprint.add_url_rule(
    "/change_admin_rights/",
    endpoint="create_admin",
    methods=["POST"],
    view_func=ChangeSuperuserRights.as_view("user_role")
)

user_role_blueprint.add_url_rule(
    "/change_admin_rights/<string:user_id>",
    endpoint="delete_admin",
    methods=["DELETE"],
    view_func=ChangeSuperuserRights.as_view("user_role")
)



