import secrets
import string

from app.services.auth_services.jwt_service import JWT_SERVICE
from app.services.auth_services.storages import REF_TOK_STORAGE
from app.services.storage.storage import user_table, user_login_history_table
from app.utils.exceptions import NotFoundError


class OauthService:
    @staticmethod
    def process_oauth(oauth_user_id: str, oauth_type: str, agent: str):
        try:
            user = user_table.read({"oauth_id": oauth_user_id, "oauth_type": oauth_type})
            user_id = user["id"]
        except NotFoundError:
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(20))

            user_data = {
                "login": oauth_type + oauth_user_id,
                "password": password,
                "oauth_id": oauth_user_id,
                "oauth_type": oauth_type
            }
            user_id = user_table.create(user_data)

        access_token, refresh_token = JWT_SERVICE.generate_tokens(
            user_id=user_id,
        )

        REF_TOK_STORAGE.add_token(
            token=refresh_token,
            agent=agent,
            user_id=user_id
        )

        user_login_history_table.create(
            data={
                "user_id": user_id,
                "user_agent": agent,
                "refresh_token": refresh_token,
            }
        )

        return access_token, refresh_token


oauth_service = OauthService()
