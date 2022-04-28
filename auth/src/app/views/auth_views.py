from flask import Blueprint
from flasgger.utils import swag_from

from app.core.swagger_config import SWAGGER_DOCS_RELATIVE_PATH

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth/api/v1')


@auth_blueprint.route('/login/', endpoint='login', methods=['POST'])
@swag_from(f'{SWAGGER_DOCS_RELATIVE_PATH}/auth/login.yaml', endpoint='auth.login', methods=['POST'])
def login():
    return "", 200


@auth_blueprint.route('/logout/<string:user_id>', endpoint='logout', methods=['POST'])
@swag_from(f'{SWAGGER_DOCS_RELATIVE_PATH}/auth/logout.yaml', endpoint='auth.logout', methods=['POST'])
def logout():
    return "", 200


@auth_blueprint.route('/logout_all/<string:user_id>', endpoint='logout-all', methods=['POST'])
@swag_from(f'{SWAGGER_DOCS_RELATIVE_PATH}/auth/logout_all.yaml', endpoint='auth.logout-all', methods=['POST'])
def logout_all():
    return "", 200


@auth_blueprint.route('/authorize/', endpoint='authorize', methods=['POST'])
@swag_from(f'{SWAGGER_DOCS_RELATIVE_PATH}/auth/authorize.yaml', endpoint='auth.authorize', methods=['POST'])
def authorize():
    return "", 200