import json

import os

from typing import Optional
from uuid import UUID

from dotenv import load_dotenv
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import HTTPException

from blueprints.auth import auth_bp
from blueprints.cli import command_bp
from blueprints.user import user_bp
from helpers.redis import jwt_redis_blocklist
from models import User
from settings.config import configurations
from settings.extensions import db, migrate, jwt, mobility, cache, logger

load_dotenv('../.env')

API_URL = os.getenv('FLASK_BASE_URL') + '/static/swagger-schema.yaml'

app = Flask(__name__)

SWAGGER_URL = '/api/docs'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={'app_name': 'Test application'}
)
app.register_blueprint(swaggerui_blueprint)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=['2000000 per day', '500000 per hour'],
)

app.config.from_object(configurations['dev'])
db.init_app(app)
jwt.init_app(app)
mobility.init_app(app)
migrate.init_app(app, db, render_as_batch=True)
cache.init_app(app)


app.register_blueprint(auth_bp, url_prefix='/v1')
app.register_blueprint(user_bp, url_prefix='/v1/user')
app.register_blueprint(command_bp)


@app.route('/')
def index() -> str:
    return 'Hi there! from API v.1.0'


@jwt.user_identity_loader
def user_identity_lookup(user) -> UUID:
    return user.id


@jwt.user_lookup_loader
@cache.memoize(timeout=60)
def user_lookup_callback(_jwt_header, jwt_data) -> Optional[User]:
    """
    Makes current_user variable available in every endpoint with @jwt_required
    """
    identity = jwt_data['sub']
    return User.query.filter_by(id=identity).one_or_none()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) -> bool:
    """
    Callback function to check if a JWT exists in the redis blocklist
    """
    jti = jwt_payload['jti']
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@app.errorhandler(HTTPException)
def exceptions(e: HTTPException):
    logger.error(e)
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response
