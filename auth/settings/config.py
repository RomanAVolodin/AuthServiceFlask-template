import os
from datetime import timedelta

JWT_ACCESS_EXPIRES = timedelta(
    hours=int(os.getenv('FLASK_JWT_EXPIRES_HOURS', 1))
)
JWT_REFRESH_EXPIRES = timedelta(
    days=int(os.getenv('FLASK_REFRESH_EXPIRES_DAYS', 15))
)

JWT_REDIS_HOST = os.getenv('FLASK_REDIS_HOST', 'localhost')
JWT_REDIS_PORT = os.getenv('FLASK_REDIS_PORT', 6379)


class BaseConfig:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'secret01')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("FLASK_DB_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'
    JWT_SECRET_KEY = os.getenv('FLASK_JWT_KEY', 'super-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = JWT_ACCESS_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = JWT_REFRESH_EXPIRES


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProdConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_ECHO = True


configurations = {'dev': DevConfig, 'prod': ProdConfig}
