import os

from app.core import app
from app.views.user_view import user_blueprint

app.register_blueprint(user_blueprint)


if __name__ == "__main__":
    app.run(host=os.getenv('HOST', 'localhost'))
