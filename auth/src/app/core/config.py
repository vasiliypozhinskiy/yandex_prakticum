import os

from pydantic import BaseSettings, Field

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
    RATE_LIMIT = int(os.getenv("RPM_LIMIT", 10))
    RATE_LIMIT_SESSION_LEN = int(os.getenv("RATE_LIMIT_SESSION_LEN", 60*60))


class TracingConfig(BaseSettings):
    sampling_rate: float = Field(0.05, env='TRACE_SAMPLING_FREQUENCY')
    agent_port: int = Field(6831, env='TRACING_AGENT_PORT')
    host: str = Field("tracing", env='TRACING_HOST')
    log: bool = Field(True, env='LOG_TRACING')
