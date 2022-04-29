import json

from flask import Blueprint, jsonify, request
from flasgger.utils import swag_from

from app.core.swagger_config import SWAGGER_DOCS_RELATIVE_PATH
from app.views.models.auth import AuthReqView, AuthRespView
from app.models.db_models import User as DBUserModel
from app.utils.utils import check_password
from app.services.auth_services.jwt_service import JWT_SERVICE
from app.services.auth_services.storages import REF_TOK_STORAGE
from app.services.auth_services.black_list import REVOKED_ACCESS

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth/api/v1')


@auth_blueprint.route('/login/', endpoint='login', methods=['POST'])
# @swag_from(f'{SWAGGER_DOCS_RELATIVE_PATH}/auth/login.yaml', endpoint='auth.login', methods=['POST'])
def login():
    request_data = request.json
    try:
        login_data = AuthReqView.parse_obj(request_data)
    except Exception as err:
        return err.messages, 400

    creds_from_storage = DBUserModel.query.filter_by(login=login_data.login).first()
    if creds_from_storage is None:
        return "invalid login", 404

    if check_password(
        password=login_data.password, hashed_password=creds_from_storage.password
    ): 

        # TODO write login info to relation db
        access_token, refresh_token = JWT_SERVICE.generate_tokens(
            user_id=creds_from_storage.id,
        )
        REF_TOK_STORAGE.add_token(refresh_token)
        out = AuthRespView(access_token=access_token, refresh_token=refresh_token)
        return jsonify(json.loads(out.json())), 200
    else:
        return "wrong password", 403


@auth_blueprint.route('/logout', endpoint='logout', methods=['POST'])
@swag_from(f'{SWAGGER_DOCS_RELATIVE_PATH}/auth/logout.yaml', endpoint='auth.logout', methods=['POST'])
def logout():
    access_token = request.headers.get("Authorization") or ""
    
    print("access_token got", flush=True)
    payload = JWT_SERVICE.get_access_payload(access_token)
    if payload is not None:
        REVOKED_ACCESS.add(access_token)

        return ("", 200)
    else:
        return ("", 403)


@auth_blueprint.route('/logout_all/<string:user_id>', endpoint='logout-all', methods=['POST'])
@swag_from(f'{SWAGGER_DOCS_RELATIVE_PATH}/auth/logout_all.yaml', endpoint='auth.logout-all', methods=['POST'])
def logout_all():
    return "", 200


@auth_blueprint.route('/authorize/', endpoint='authorize', methods=['POST'])
@swag_from(f'{SWAGGER_DOCS_RELATIVE_PATH}/auth/authorize.yaml', endpoint='auth.authorize', methods=['POST'])
def authorize():
    access_token = request.headers.get("Authorization") or ""
    payload = JWT_SERVICE.get_access_payload(access_token)
    if payload is not None:
        if REVOKED_ACCESS.is_ok(access_token):
            return (jsonify(payload.roles), 200)
    return ("", 403)