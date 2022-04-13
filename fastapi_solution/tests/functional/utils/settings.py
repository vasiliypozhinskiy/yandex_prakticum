from pydantic import BaseSettings, Field
from typing import Optional


class TestSettings(BaseSettings):
    es_host: str = Field("http://localhost:9200", env="ELASTIC_HOST")
    es_user: str = Field("elastic", env="ELASTIC_USER")
    es_password: Optional[str] = Field(env="ELASTIC_PASSWORD")
    redis_host: str = Field("redis://localhost", env="REDIS_HOST")
    redis_port: str = Field("6379", env="REDIS_PORT")
    redis_password: Optional[str] = Field(env="REDIS_PASSWORD")
    service_url: str = Field("http://localhost:8000", env="SERVICE_URL")
    api_url: str = Field("/api/v1")
