from flask import Blueprint
from flask import jsonify
from flask import request
from flasgger.utils import swag_from

from app.core.swagger_config import SWAGGER_DOCS_RELATIVE_PATH
from app.services.user_service import UserService
from app.utils.exceptions import FieldValidationError, AlreadyExistsError, BadPasswordError, BadEmailError, \
    BadLengthError, BadIdFormat, NotFoundError
from app.utils.logger import logger
from app.utils.utils import hide_password
from app.views.models.user import UserResponse

user_blueprint = Blueprint('user', __name__, url_prefix='/auth/api/v1')


@user_blueprint.route('/user/', endpoint='create_user', methods=['POST'])
@user_blueprint.route('/user/<string:user_id>', endpoint='user_with_id', methods=['GET', 'PATCH', 'DELETE'])
@swag_from(f'{SWAGGER_DOCS_RELATIVE_PATH}/user/create_user.yaml', endpoint='user.create_user')
@swag_from(f'{SWAGGER_DOCS_RELATIVE_PATH}/user/get_user.yaml', endpoint='user.user_with_id', methods=['GET'])
@swag_from(f'{SWAGGER_DOCS_RELATIVE_PATH}/user/update_user.yaml', endpoint='user.user_with_id', methods=['PATCH'])
@swag_from(f'{SWAGGER_DOCS_RELATIVE_PATH}/user/delete_user.yaml', endpoint='user.user_with_id', methods=['DELETE'])
def user_request_handler(user_id: str = None):
    if request.method == 'POST':
        response = create_user(request)
    elif request.method == 'GET':
        response = get_user(user_id)
    elif request.method == 'PATCH':
        response = update_user(request, user_id)
    elif request.method == 'DELETE':
        response = delete_user(user_id)
    else:
        return 'Method not allowed', 405

    return response


def create_user(request_):
    """Метод для регистрации пользователя
    """
    user_data = request_.json

    service = UserService()

    try:
        service.create_user(user_data)
    except BadPasswordError as e:
        return e.message, 400
    except BadEmailError as e:
        return e.message, 400
    except BadLengthError as e:
        return e.message, 400
    except FieldValidationError as e:
        logger.error(f'Can\'t create user with params: {hide_password(user_data)}')
        return e.message, 400
    except AlreadyExistsError:
        return 'Resource already exists', 409
    return 'Created', 201


def get_user(user_id: str):
    """Метод для получения данных пользователя по id
    """
    try:
        service = UserService()

        user = service.get_user(user_id)
        if not user:
            return 'Not found', 404

        response = UserResponse(
            id=user.id,
            login=user.login,
            is_superuser=user.is_superuser,
            email=user.email,
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name,
        )
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
    """Метод для обновления данных пользователя (кроме пароля) по id
    """
    service = UserService()
    user_data = request_.json

    try:
        service.update_user(user_id, user_data)
    except NotFoundError as e:
        return e.message, 404
    except BadEmailError as e:
        return e.message, 400
    except BadLengthError as e:
        return e.message, 400
    except BadIdFormat as e:
        return e.message, 400
    except FieldValidationError as e:
        logger.error(f'Can\'t update user with params: {user_data}')
        return e.message, 400
    except AlreadyExistsError:
        return 'Resource already exists', 409

    return 'User updated', 200


def delete_user(user_id: str):
    """Метод для удаления пользователя по id
    """
    service = UserService()

    try:
        service.delete_user(user_id)
    except NotFoundError as e:
        return e.message, 404
    except BadIdFormat as e:
        return e.message, 400

    return 'User deleted', 200
