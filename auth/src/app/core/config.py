import os

DB_PORT = os.getenv('DB_PORT', 4321)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.environ.get('DEBUG', False) == 'True'
    SQLALCHEMY_DATABASE_URI = f'postgresql://auth_app:123qwe@172.18.0.4:4321/auth_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
