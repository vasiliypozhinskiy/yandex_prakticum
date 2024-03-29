import os
from logging import config as logging_config

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

REDIS_HOST = os.getenv('REDIS_HOST', 'redis://localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

ELASTIC_HOST = os.getenv('ELASTIC_HOST', 'http://localhost')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))
ELASTIC_PASSWORD = os.getenv('ELASTIC_PASSWORD')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Время работы кэша
CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут