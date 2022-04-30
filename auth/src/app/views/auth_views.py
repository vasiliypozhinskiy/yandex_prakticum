import json
import uuid
from typing import Optional

from flask import Blueprint, jsonify, request
from flasgger.utils import swag_from
from pydantic import ValidationError

from app.utils.exceptions import AccessDenied, UnExistingLogin, InvalidToken
from app.core.swagger_config import SWAGGER_DOCS_RELATIVE_PATH
from app.views.models.auth import AuthReqView
from app.services.auth_services.auth_services import AUTH_SERVICE

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth/api/v1')


@auth_blueprint.route('/login/', endpoint='login', methods=['POST'])
@swag_from(f'{SWAGGER_DOCS_RELATIVE_PATH}/auth/login.yaml', endpoint='auth.login', methods=['POST'])
def login():
    request_data = request.json
    try:
        login_data = AuthReqView.parse_obj(request_data)
    except ValidationError as e:
        return str(e), str(e)

    try:
        login_resp = AUTH_SERVICE.login(login_data)
    except UnExistingLogin as e:
        return str(e), 404
    except AccessDenied as e:
        return str(e), 403
    except ValidationError as e:
        return str(e), 400
    return jsonify(json.loads(login_resp.json())), 200



@auth_blueprint.route('/logout', endpoint='logout', methods=['POST'])
@swag_from(f'{SWAGGER_DOCS_RELATIVE_PATH}/auth/logout.yaml', endpoint='auth.logout', methods=['POST'])
def logout():
    access_token = request.headers.get("Authorization", "")
    try:
        AUTH_SERVICE.logout(access_token=access_token)
        return '', 200
    except InvalidToken as e:
        return str(e), 403


@auth_blueprint.route('/logout_all/', endpoint='logout-all', methods=['POST'])
@auth_blueprint.route('/logout_all/<string:user_id>', endpoint='logout-all', methods=['POST'])
@swag_from(f'{SWAGGER_DOCS_RELATIVE_PATH}/auth/logout_all.yaml', endpoint='auth.logout-all', methods=['POST'])
@swag_from(f'{SWAGGER_DOCS_RELATIVE_PATH}/auth/logout_all_id.yaml', endpoint='auth.logout-all', methods=['POST'])
def logout_all(user_id: Optional[str] = None):
    access_token = request.headers.get("Authorization", "")
    try:
        if user_id is not None:
            user_id = uuid.UUID(user_id)
        AUTH_SERVICE.logout_all(access_token=access_token, user_id=user_id)
        return '', 200
    except InvalidToken as e:
        return str(e), 403


@auth_blueprint.route('/authorize/', endpoint='authorize', methods=['POST'])
@swag_from(f'{SWAGGER_DOCS_RELATIVE_PATH}/auth/authorize.yaml', endpoint='auth.authorize', methods=['POST'])
def authorize():
    access_token = request.headers.get("Authorization", "")
    try:
        roles = AUTH_SERVICE.authorize(access_token=access_token)
        return (jsonify(roles), 200)
    except InvalidToken as e:
        return str(e), 403
    return ("", 403)