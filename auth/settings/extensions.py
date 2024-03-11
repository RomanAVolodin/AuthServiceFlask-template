import os
import logging

from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_mobility import Mobility
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_caching import Cache

from settings.config import JWT_REDIS_HOST, JWT_REDIS_PORT


naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}


db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
mobility = Mobility()

cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': JWT_REDIS_HOST,
    'CACHE_REDIS_PORT': JWT_REDIS_PORT
})

logger = logging.getLogger('Auth app logger')
logger.setLevel(logging.INFO)
