from urllib.parse import urlencode
from http import HTTPStatus

import requests
from flasgger import swag_from
from flask import Blueprint, request
from flask.views import MethodView

from app.core.swagger_config import SWAGGER_DOCS_PATH
from app.core.config import YandexOathConfig, VKOathConfig
from app.services.oauth_service import vk_oauth_service, yandex_oauth_service
from app.views.utils.decorator import catch_exceptions
from app.utils.exceptions import AccessDenied

oauth_blueprint = Blueprint('oauth', __name__, url_prefix='/auth/api/v1/oauth')

yandex_oauth_config = YandexOathConfig()
vk_oauth_config = VKOathConfig()


class VKOauthView(MethodView):
    @swag_from(
        f"{SWAGGER_DOCS_PATH}/oauth/vk.yaml",
        endpoint="oauth.vk_auth",
        methods=["GET"]
    )
    @catch_exceptions
    def get(self):
        params = {
            "client_id": vk_oauth_config.client_id,
            "redirect_uri": vk_oauth_config.redirect_url,
            "display": "page",
            "response_type": "code"
        }
        vk_url_params = urlencode(params)
        url = f"{vk_oauth_config.auth_url}?{vk_url_params}"

        return {"url": url}, 200


class YandexOauthView(MethodView):
    @swag_from(
        f"{SWAGGER_DOCS_PATH}/oauth/vk.yaml",
        endpoint="oauth.vk_auth",
        methods=["GET"]
    )
    @catch_exceptions
    def get(self):
        params = {
            "client_id": yandex_oauth_config.client_id,
            "redirect_uri": yandex_oauth_config.redirect_url,
            "display": "page",
            "response_type": "code"
        }
        url_params = urlencode(params)
        url = f"{yandex_oauth_config.auth_url}?{url_params}"

        return {"url": url}, 200


class YandexLoginView(MethodView):

    @catch_exceptions
    def get(self):
        tokens = yandex_oauth_service.login(
            code=request.args["code"],
            agent=request.headers.get("USER_AGENT", "empty-agent")
        )
        return {
            "access_token": tokens.access_token,
            "refresh_token": tokens.refresh_token
        }, HTTPStatus.OK


class VKLoginView(MethodView):

    @catch_exceptions
    def get(self):
        tokens = vk_oauth_service.login(
            code=request.args["code"],
            agent=request.headers.get("USER_AGENT", "empty-agent")
        )
        return {
            "access_token": tokens.access_token,
            "refresh_token": tokens.refresh_token
        }, HTTPStatus.OK
        

oauth_blueprint.add_url_rule(
    '/vk/login/',
    endpoint='vk_login',
    view_func=VKLoginView.as_view('auth'),
    methods=["GET"]
)
oauth_blueprint.add_url_rule(
    '/yandex/login/',
    endpoint='yandex_login',
    view_func=YandexLoginView.as_view('auth'),
    methods=["GET"]
)

oauth_blueprint.add_url_rule(
    '/vk/auth/',
    endpoint='vk_auth',
    view_func=VKOauthView.as_view('auth'),
    methods=["GET"]
)
oauth_blueprint.add_url_rule(
    '/yandex/auth/',
    endpoint='yandex_auth',
    view_func=YandexOauthView.as_view('auth'),
    methods=["GET"]
)