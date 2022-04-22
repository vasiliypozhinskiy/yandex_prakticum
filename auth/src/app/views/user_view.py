from flask import Blueprint
from flask import jsonify
from flask import request

from app.services.user_service import UserService
from app.utils.exceptions import ValidationError, AlreadyExistsError, BadPasswordError, BadEmailError, BadLengthError
from app.utils.logger import logger
from app.utils.utils import remove_password
from app.views.models.user import UserResponse

user_blueprint = Blueprint('user', __name__, url_prefix='/auth/api/v1')


@user_blueprint.route('/user/', methods=['POST'])
def create_user():
    """Метод для регистрации пользователя
    ---
    parameters:
        - in: body
          name: user
          description: Данные пользователя
          schema:
            type: object
            required:
              - login
              - password
              - email
            properties:
              login:
                type: string
                example: login
              password:
                type: string
                example: 123qweQWE!@#
              email:
                type: string
                example: example@email.com
              first_name:
                type: string
                example: Иван
              middle_name:
                type: string
                example: Иванович
              last_name:
                type: string
                example: Иванов
    responses:
        201:
            description: Пользователь зарегестрирован
        400:
            description: Неправильные параметры запроса
        409:
            description: Пользователь с таким имейлом или логином уже зарегестрирован
    """
    user_data = request.json

    try:
        service = UserService()
        service.create_user(**user_data)
    except BadPasswordError as e:
        return e.message, 400
    except BadEmailError as e:
        return e.message, 400
    except BadLengthError as e:
        return e.message, 400
    except ValidationError:
        logger.error(f'Can\'t create user with params: {remove_password(user_data)}')
        return 'Bad request params', 400
    except AlreadyExistsError:
        return 'Resource already exists', 409
    return 'Created', 201


@user_blueprint.route('/user/<user_id>')
def get_user(user_id):
    """Метод для получения пользователя по id
    ---
    parameters:
      - in: path
        name: user_id
        description: id пользователя (UUID)
        schema:
          type: string
    responses:
        200:
            description: Данные пользователя
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    login:
                      type: string
                      example: login
                    password:
                      type: string
                      example: 123qweQWE!@#
                    email:
                      type: string
                      example: example@email.com
                    first_name:
                      type: string
                      example: Иван
                    middle_name:
                      type: string
                      example: Иванович
                    last_name:
                      type: string
                      example: Иванов
    """
    try:
        service = UserService()
        user = service.get_user(user_id)
        response = UserResponse(
            id=user.id,
            login=user.login,
            is_superuser=user.is_superuser,
            email=user.email,
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name,
        )
    except Exception as e:
        return e
    return jsonify(dict(response))
