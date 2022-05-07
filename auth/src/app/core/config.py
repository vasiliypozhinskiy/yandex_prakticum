import os

DB_PORT = os.getenv("DB_PORT", 4321)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

SECRET_SIGNATURE = os.getenv("SECRET_SIGNATURE", "secret")


ACCESS_TOKEN_EXP = 60 * 60 * 10
REFRESH_TOKEN_EXP = 60 * 60 * 24 * 7

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

TEMPLATE_FOLDER = os.getcwd() + "/templates"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.environ.get("DEBUG", False) == "True"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://auth_app:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/auth_database"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TRACE_SAMPLING_FREQUENCY = float(os.getenv("TRACE_SAMPLING_FREQUENCY", 5)) / 100