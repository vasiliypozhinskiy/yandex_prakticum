from app.core.swagger_config import SWAGGER_DOCS_PATH
from app.services.auth_services.jwt_service import JWT_SERVICE
from app.services.role_service import role_service
from app.utils.exceptions import AlreadyExistsError
from app.utils.exceptions import NotFoundError
from flasgger.utils import swag_from
from flask import Blueprint, request

role_blueprint = Blueprint("role", __name__, url_prefix="/auth/api/v1")


@role_blueprint.route(
    "/role/<string:new_role>", endpoint="create_role", methods=["POST"]
)
@role_blueprint.route("/role/role_list/", endpoint="list_role", methods=["GET"])
@role_blueprint.route(
    "/role/<string:role_title>", endpoint="delete_role", methods=["DELETE"]
)
@role_blueprint.route(
    "/role/<string:role_title>/<new_role>", endpoint="update_role", methods=["PATCH"]
)
@swag_from(
    f"{SWAGGER_DOCS_PATH}/role/create_role.yaml", endpoint="role.create_role"
)
@swag_from(
    f"{SWAGGER_DOCS_PATH}/role/delete_role.yaml",
    endpoint="role.delete_role",
    methods=["DELETE"],
)
@swag_from(
    f"{SWAGGER_DOCS_PATH}/role/get_list_role.yaml",
    endpoint="role.list_role",
    methods=["GET"],
)
@swag_from(
    f"{SWAGGER_DOCS_PATH}/role/update_role.yaml",
    endpoint="role.update_role",
    methods=["PATCH"],
)
def role_handler(new_role: str = None, role_title: str = None):
    if request.method == "POST":
        response = create_role(new_role)
    elif request.method == "GET":
        response = get_list_role()
    elif request.method == "PATCH":
        response = update_role(role_title, new_role)
    elif request.method == "DELETE":
        response = delete_role(role_title)
    else:
        return "Method not allowed", 405
    return response


@JWT_SERVICE.token_required(check_is_superuser=True)
def create_role(new_role):
    """
    Метод для создания роли
    """
    role = {"title": new_role}
    try:
        role_service.create_role(role)
    except AlreadyExistsError as e:
        return e.message, 409
    return "Created", 201


def get_list_role():
    roles = role_service.get_list_role()
    return roles


@JWT_SERVICE.token_required(check_is_superuser=True)
def update_role(role_title: str, new_role: str):
    try:
        role_service.update_role(role_title, new_role)
    except NotFoundError as e:
        return e.message, 404
    except AlreadyExistsError as e:
        return e.message, 409
    return "Role updated", 200


@JWT_SERVICE.token_required(check_is_superuser=True)
def delete_role(role_title):
    """Метод для удаления роли"""
    try:
        role_service.delete_role(role_title)
    except NotFoundError as e:
        return e.message, 404
    return "Role deleted", 200
