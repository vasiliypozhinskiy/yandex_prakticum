import os

from app.core import app
from app.views.user_view import user_blueprint
from app.views.role_view import role_blueprint
from app.views.user_add_role import add_role_blueprint

app.register_blueprint(user_blueprint)
app.register_blueprint(role_blueprint)
app.register_blueprint(add_role_blueprint)


if __name__ == "__main__":
    app.run(
        host=os.getenv('HOST', 'localhost'),
        debug=bool(os.getenv('DEBUG', 1))
    )
