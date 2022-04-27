import os

from dotenv import load_dotenv

load_dotenv()

DB_PORT = os.getenv('AUTH_DB_PORT', 4321)
DB_HOST = os.getenv('AUTH_DB_HOST', 'localhost')
DB_PASSWORD = os.getenv('AUTH_DB_PASSWORD', '')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.environ.get('DEBUG', False) == 'True'
    SQLALCHEMY_DATABASE_URI = f'postgresql://auth_app:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/auth_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
