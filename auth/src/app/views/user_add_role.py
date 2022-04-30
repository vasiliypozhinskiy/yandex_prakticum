from flask import request, Blueprint
from flasgger.utils import swag_from

from app.models.db_models import User, Role
from app.core import db

from app.core.swagger_config import SWAGGER_DOCS_PATH
from app.services.auth_services.auth_services import AUTH_SERVICE
from app.utils.exceptions import NotFoundError, AlreadyExistsError

from app.utils.utils import check_password


add_role_blueprint = Blueprint("role_add_user", __name__, url_prefix="/auth/api/v1")


@add_role_blueprint.route(
    "/user_add_role/<string:user_id>/<string:role_title>",
    endpoint="add_role",
    methods=["POST"],
)
@add_role_blueprint.route(
    "/user_delete_role/<string:user_id>/<string:role_title>",
    endpoint="delete_role",
    methods=["DELETE"],
)
@swag_from(
    f"{SWAGGER_DOCS_PATH}/role/add_role_for_user.yaml",
    endpoint="role_add_user.add_role",
)
@swag_from(
    f"{SWAGGER_DOCS_PATH}/role/remove_role_for_user.yaml",
    endpoint="role_add_user.delete_role",
)
def user_add_delete_role(user_id: str, role_title: str):
    try:
        if request.method == "POST":
            add_role(user_id, role_title)
            return "Роль успешно добавленна", 200
        elif request.method == "DELETE":
            delete_role(user_id, role_title)
            return "Роль успешно удалена", 200
        else:
            return "Method not allowed", 405
    except NotFoundError as e:
        return e.message, 404
    except AlreadyExistsError as e:
        return e.message, 409


@AUTH_SERVICE.token_required(check_is_superuser=True)
def delete_role(user_id: str = None, role_title: str = None):
    user = User.query.filter_by(id=user_id).first()
    role = Role.query.filter_by(title=role_title).first()
    user.roles.remove(role)
    db.session.commit()


@AUTH_SERVICE.token_required(check_is_superuser=True)
def add_role(user_id: str = None, role_title: str = None):
    user = User.query.filter_by(id=user_id).first()
    role = Role.query.filter_by(title=role_title).first()
    if not user or not role:
        raise NotFoundError("Role or user not found")
    list_roles_in_user = [x.title for x in user.roles]
    if role.title in list_roles_in_user:
        return AlreadyExistsError("Role already exist")
    user.roles.append(role)
    db.session.commit()


@add_role_blueprint.route(
    "/change_admin_rights/",
    endpoint="create_admin",
    methods=["POST"],
)
@add_role_blueprint.route(
    "/change_admin_rights/<string:user_id>",
    endpoint="delete_admin",
    methods=["DELETE"],
)
@swag_from(
    f"{SWAGGER_DOCS_PATH}/role/create_admin.yaml",
    endpoint="role_add_user.create_admin",
)
@swag_from(
    f"{SWAGGER_DOCS_PATH}/role/delete_admin.yaml",
    endpoint="role_add_user.delete_admin",
)
def change_superuser_rights(user_id: str = None):
    try:
        if request.method == "POST":
            create_admin()
            return "Admin created", 200
        if request.method == "DELETE":
            delete_admin(user_id)
            return "Admin deleted", 200
    except NotFoundError as e:
        return e.message, 404
    except AlreadyExistsError as e:
        return e.message, 409


@AUTH_SERVICE.token_required(check_is_superuser=True)
def create_admin():
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


@AUTH_SERVICE.token_required(check_is_superuser=True)
def delete_admin(user_id: str):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        raise NotFoundError("User not found")
    if not user.is_superuser:
        raise AlreadyExistsError("")

    # Логика для отправки email с ссылкой для подтверждения действия
    db.session.query(User).get(user_id).is_superuser = False
    db.session.commit()



