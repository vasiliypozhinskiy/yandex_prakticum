from flask import request, Blueprint
from flasgger.utils import swag_from

from app.models.db_models import User, Role
from app.core import db

from app.core.swagger_config import SWAGGER_DOCS_RELATIVE_PATH

from app.utils.utils import check_password

add_role_blueprint = Blueprint("role_add_user", __name__, url_prefix="/auth/api/v1")


@add_role_blueprint.route(
    "/user_add_role/<string:user_id>/<string:role_title>",
    endpoint="add_role",
    methods=["POST", "DELETE"],
)
@swag_from(
    f"{SWAGGER_DOCS_RELATIVE_PATH}/role/add_role_for_user.yaml",
    endpoint="role_add_user.add_role",
)
@swag_from(
    f"{SWAGGER_DOCS_RELATIVE_PATH}/role/remove_role_for_user.yaml",
    endpoint="role_add_user.add_role",
)
def user_add_delete_role(user_id: str = None, role_title: str = None):
    user = User.query.filter_by(id=user_id).first()
    role = Role.query.filter_by(title=role_title).first()
    if request.method == "POST":
        if not user or not role:
            return "Данные пользователя или роли не найдены", 406
        list_roles_in_user = [x.title for x in user.roles]
        if role.title in list_roles_in_user:
            return "Роль уже существует у пользователя", 409
        user.roles.append(role)
        db.session.commit()
        return "Роль успешно добавленна", 200
    elif request.method == "DELETE":
        user.roles.remove(role)
        db.session.commit()
        return "Роль успешно удалена", 200
    else:
        return "Method not allowed", 405


@add_role_blueprint.route(
    "/create_admin/",
    endpoint="create_admin",
    methods=["POST"],
)
@swag_from(
    f"{SWAGGER_DOCS_RELATIVE_PATH}/role/create_admin.yaml",
    endpoint="role_add_user.create_admin",
)
def create_admin():
    if request.method == "POST":
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        if user.is_superuser:
            return 'Пользователь уже администратор', 409
        if user and check_password(data['password'], user.password):
            # Логика для отправки email с ссылкой для подтверждения действия
            db.session.query(User).get(user.id).is_superuser = True
            db.session.commit()
            return 'Администратор успешно создан', 200
        return 'Проверьте параметры запроса', 404
