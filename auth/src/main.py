import os

from app.core import app, db, migrate, Config
from app.views.user_view import user_blueprint
from app.views.role_view import role_blueprint
from app.views.user_add_role import user_role_blueprint
from app.views.auth_views import auth_blueprint


def create_app(flask_app):
    db.init_app(flask_app)
    flask_app.register_blueprint(role_blueprint)
    flask_app.register_blueprint(user_role_blueprint)
    flask_app.register_blueprint(user_blueprint)
    flask_app.register_blueprint(auth_blueprint)
    migrate.init_app(flask_app, db)
    flask_app.run(
        host=os.getenv('HOST', 'localhost'),
        debug=bool(os.getenv('DEBUG', 1)),
    )

if __name__ == "__main__":
    create_app(flask_app=app)