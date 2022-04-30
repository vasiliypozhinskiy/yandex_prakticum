from app.core.swagger_config import SWAGGER_DOCS_PATH
from app.services.user_service import user_service
from app.services.auth_services.jwt_service import JWT_SERVICE
from app.services.auth_services.auth_services import AUTH_SERVICE
from app.utils.exceptions import (
    FieldValidationError,
    AlreadyExistsError,
    BadPasswordError,
    BadEmailError,
    BadLengthError,
    BadIdFormat,
    NotFoundError, AccessDenied, InvalidToken,
)
from app.views.models.user import UserResponse
from flasgger.utils import swag_from
from flask import Blueprint, jsonify, request


user_blueprint = Blueprint("user", __name__, url_prefix="/auth/api/v1")


@user_blueprint.route("/user/", endpoint="create_user", methods=["POST"])
@user_blueprint.route(
    "/user/<string:user_id>",
    endpoint="user_with_id",
    methods=["GET", "PATCH", "DELETE"],
)
@swag_from(
    f"{SWAGGER_DOCS_PATH}/user/create_user.yaml", endpoint="user.create_user"
)
@swag_from(
    f"{SWAGGER_DOCS_PATH}/user/get_user.yaml",
    endpoint="user.user_with_id",
    methods=["GET"],
)
@swag_from(
    f"{SWAGGER_DOCS_PATH}/user/update_user.yaml",
    endpoint="user.user_with_id",
    methods=["PATCH"],
)
@swag_from(
    f"{SWAGGER_DOCS_PATH}/user/delete_user.yaml",
    endpoint="user.user_with_id",
    methods=["DELETE"],
)
def user_request_handler(user_id: str = None):
    try:
        if request.method == "POST":
            response = create_user(request)
        elif request.method == "GET":
            response = get_user(user_id)
        elif request.method == "PATCH":
            response = update_user(request, user_id=user_id)
        elif request.method == "DELETE":
            response = delete_user(user_id)
        else:
            return "Method not allowed", 405

    except NotFoundError as e:
        return e.message, 404
    except (BadEmailError, BadLengthError, BadIdFormat, BadPasswordError, FieldValidationError) as e:
        return e.message, 400
    except InvalidToken as e:
        return e.message, 401
    except AccessDenied as e:
        return e.message, 403
    except AlreadyExistsError as e:
        return e.message, 409
    return response


def create_user(request_):
    """Метод для регистрации пользователя"""
    user_data = request_.json

    new_user_id = user_service.create_user(user_data)

    return {"user_id": new_user_id}, 201


def get_user(user_id: str):
    """Метод для получения данных пользователя по id"""
    user = user_service.get_user(user_id)
    if not user:
        raise NotFoundError

    if user.birthdate:
        user.birthdate = user.birthdate.strftime('%Y-%m-%d')

    response = UserResponse.parse_obj(user)

    return jsonify(dict(response))


@JWT_SERVICE.token_required(check_is_me=True)
def update_user(request_, user_id: str):
    """Метод для обновления данных пользователя (кроме пароля) по id"""
    user_data = request_.json

    user_service.update_user(user_id, user_data)

    return "User updated", 200


@JWT_SERVICE.token_required(check_is_me=True)
def delete_user(user_id: str):
    """Метод для удаления пользователя по id"""
    user_service.delete_user(user_id)
    AUTH_SERVICE.logout_all(request.headers["authorization"])

    return "User deleted", 200


@user_blueprint.route("/user/<string:user_id>/change_password", endpoint="change_password", methods=["PUT"])
@swag_from(
    f"{SWAGGER_DOCS_PATH}/user/change_password.yaml", endpoint="user.change_password"
)
@JWT_SERVICE.token_required(check_is_me=True)
def user_password(user_id):
    passwords = request.json

    if not passwords.get("old_password") or passwords.get("new_password"):
        return "Wrong request params", 400

    try:
        user_service.change_password(user_id, passwords)
        AUTH_SERVICE.logout_all(request.headers["authorization"])
    except (BadIdFormat, BadPasswordError) as e:
        return e.message, 400
    except AccessDenied as e:
        return e.message, 403
    except NotFoundError as e:
        return e.message, 404

    return "Password changed", 200
