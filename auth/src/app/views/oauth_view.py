from urllib.parse import urlencode
from http import HTTPStatus

import requests
from flasgger import swag_from
from flask import Blueprint, request
from flask.views import MethodView

from app.utils.logger import logger
from app.core.swagger_config import SWAGGER_DOCS_PATH
from app.core.config import VKOathConfig, YandexOathConfig
from app.services.oauth_service import oauth_service
from app.views.utils.decorator import catch_exceptions
from app.utils.exceptions import AccessDenied

oauth_blueprint = Blueprint('oauth', __name__, url_prefix='/auth/api/v1/oauth')
vk_oauth_config = VKOathConfig()
yandex_oauth_config = YandexOathConfig()


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


class BaseOauthLoginView(MethodView):

    type_: str
    config: VKOathConfig

    @catch_exceptions
    def get(self):
        code = request.args["code"]
        get_token_params = {
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "redirect_uri": self.config.redirect_url,
            "code": code,
        }
        get_token_response = requests.get(self.config.get_token_url, params=get_token_params)
        if get_token_response.status_code == HTTPStatus.OK:
            vk_user_data = get_token_response.json()
            user_id = vk_user_data["user_id"]
            
            access_token, refresh_token = oauth_service.process_oauth(
                str(user_id),
                self.type_,
                request.headers.get("USER_AGENT")
            )
            return {"access_token": access_token, "refresh_token": refresh_token}, HTTPStatus.OK
        else:
            return get_token_response.text, get_token_response.status_code


class VKOauthLoginView(BaseOauthLoginView):
    
    config = vk_oauth_config
    type_ = 'VK'

    @swag_from(
        f"{SWAGGER_DOCS_PATH}/oauth/login.yaml",
        endpoint="oauth.vk_login",
        methods=["GET"]
    )
    @catch_exceptions
    def get(self):
        return super().get()


class YandexOauthLoginView(BaseOauthLoginView):
    
    config = yandex_oauth_config
    type_ = 'yandex'

    @swag_from(
        f"{SWAGGER_DOCS_PATH}/oauth/login.yaml",
        endpoint="oauth.yandex_login",
        methods=["GET"]
    )
    @catch_exceptions
    def get(self):
        code = request.args["code"]
        get_token_params = {
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "redirect_uri": self.config.redirect_url,
            "code": code,
            "grant_type": "authorization_code",
        }
        get_token_response = requests.post(
            self.config.get_token_url,
            data=get_token_params,
            headers={"Content-type": "application/x-www-form-urlencoded"}
        )
        if get_token_response.status_code == HTTPStatus.OK:
            access_token = get_token_response.json()['access_token']
            user_data = self._get_user_data(access_token=access_token)
            print(user_data, flush=True)
            user_id = user_data["id"]
            print(user_data, flush=True)
            
            access_token, refresh_token = oauth_service.process_oauth(
                str(user_id),
                self.type_,
                request.headers.get("USER_AGENT"),
            )
            return {"access_token": access_token, "refresh_token": refresh_token}, HTTPStatus.OK
        else:
            return get_token_response.text, get_token_response.status_code

    def _get_user_data(self, access_token: str):
        resp = requests.get(
            "https://login.yandex.ru/info",
            params={"oauth_token": access_token},
        )
        if resp.status_code == HTTPStatus.OK: 
            return resp.json()
        else:
            raise AccessDenied


oauth_blueprint.add_url_rule(
    '/vk/login/',
    endpoint='vk_login',
    view_func=VKOauthLoginView.as_view('auth'),
    methods=["GET"]
)
oauth_blueprint.add_url_rule(
    '/yandex/login/',
    endpoint='yandex_login',
    view_func=YandexOauthLoginView.as_view('auth'),
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