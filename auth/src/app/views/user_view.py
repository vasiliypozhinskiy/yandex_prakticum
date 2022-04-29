from app.core.swagger_config import SWAGGER_DOCS_RELATIVE_PATH
from app.services.user_service import user_service
from app.utils.exceptions import (
    FieldValidationError,
    AlreadyExistsError,
    BadPasswordError,
    BadEmailError,
    BadLengthError,
    BadIdFormat,
    NotFoundError, AccessDenied,
)
from app.utils.logger import logger
from app.utils.utils import hide_password
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
    f"{SWAGGER_DOCS_RELATIVE_PATH}/user/create_user.yaml", endpoint="user.create_user"
)
@swag_from(
    f"{SWAGGER_DOCS_RELATIVE_PATH}/user/get_user.yaml",
    endpoint="user.user_with_id",
    methods=["GET"],
)
@swag_from(
    f"{SWAGGER_DOCS_RELATIVE_PATH}/user/update_user.yaml",
    endpoint="user.user_with_id",
    methods=["PATCH"],
)
@swag_from(
    f"{SWAGGER_DOCS_RELATIVE_PATH}/user/delete_user.yaml",
    endpoint="user.user_with_id",
    methods=["DELETE"],
)
def user_request_handler(user_id: str = None):
    if request.method == "POST":
        response = create_user(request)
    elif request.method == "GET":
        response = get_user(user_id)
    elif request.method == "PATCH":
        response = update_user(request, user_id)
    elif request.method == "DELETE":
        print(user_id)
        response = delete_user(user_id)
    else:
        return "Method not allowed", 405
    return response


def create_user(request_):
    """Метод для регистрации пользователя"""
    user_data = request_.json

    try:
        new_user_id = user_service.create_user(user_data)
    except BadPasswordError as e:
        return e.message, 400
    except BadEmailError as e:
        return e.message, 400
    except BadLengthError as e:
        return e.message, 400
    except FieldValidationError as e:
        logger.error(f"Can't create user with params: {hide_password(user_data)}")
        return e.message, 400
    except AlreadyExistsError:
        return "Resource already exists", 409

    return {"user_id": new_user_id}, 201


def get_user(user_id: str):
    """Метод для получения данных пользователя по id"""
    try:
        user = user_service.get_user(user_id)
        if not user:
            return "Not found", 404

        response = UserResponse.parse_obj(user)
    except NotFoundError as e:
        return e.message, 404
    except BadEmailError as e:
        return e.message, 400
    except BadLengthError as e:
        return e.message, 400
    except BadIdFormat as e:
        return e.message, 400

    return jsonify(dict(response))


def update_user(request_, user_id: str):
    """Метод для обновления данных пользователя (кроме пароля) по id"""
    user_data = request_.json

    try:
        user_service.update_user(user_id, user_data)
    except NotFoundError as e:
        return e.message, 404
    except BadEmailError as e:
        return e.message, 400
    except BadLengthError as e:
        return e.message, 400
    except BadIdFormat as e:
        return e.message, 400
    except FieldValidationError as e:
        logger.error(f"Can't update user with params: {user_data}")
        return e.message, 400
    except AlreadyExistsError:
        return "Resource already exists", 409

    return "User updated", 200


def delete_user(user_id: str):
    """Метод для удаления пользователя по id"""
    try:
        user_service.delete_user(user_id)
    except NotFoundError as e:
        return e.message, 404
    except BadIdFormat as e:
        return e.message, 400

    return "User deleted", 200


@user_blueprint.route("/user/<string:user_id>/change_password", endpoint="change_password", methods=["PUT"])
@swag_from(
    f"{SWAGGER_DOCS_RELATIVE_PATH}/user/change_password.yaml", endpoint="user.change_password"
)
def user_password(user_id):
    passwords = request.json

    try:
        user_service.change_password(user_id, passwords)
    except BadIdFormat as e:
        return e.message, 400
    except BadPasswordError as e:
        return e.message, 400
    except AccessDenied as e:
        return e.message, 403
    except NotFoundError as e:
        return e.message, 404

    return "Password changed", 200
