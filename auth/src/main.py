import os

from app.core import app
from app.views import *

if __name__ == "__main__":
    app.run(host=os.getenv('HOST', 'localhost'))
