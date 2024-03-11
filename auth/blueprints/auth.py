from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt_extended import (
    jwt_required,
    current_user,
    get_jwt,
)

from helpers.auth_helpers import (
    add_login_history_for_user,
    generate_tokens_for_user,
)
from helpers.messages import ACCESS_TOKEN_REVOKED, WRONG_EMAIL_OR_PASSWORD
from helpers.redis import jwt_redis_blocklist
from helpers.serialization_schemas import UserSchema
from models import User, LoginHistory
from settings.config import JWT_ACCESS_EXPIRES, JWT_REFRESH_EXPIRES


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email', None)
        password = request.json.get('password', None)
    except AttributeError:
        return jsonify(WRONG_EMAIL_OR_PASSWORD), 401

    user = (
        User.query.filter(User.email == email)
        .filter(User.is_active is not False)
        .one_or_none()
    )
    if not user or not user.check_password(password):
        return jsonify(WRONG_EMAIL_OR_PASSWORD), 401

    access_token, refresh_token = generate_tokens_for_user(user)
    add_login_history_for_user(request, user, access_token, refresh_token)
    return jsonify(access=access_token, refresh=refresh_token)


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    access_token, refresh_token = generate_tokens_for_user(current_user)
    return jsonify(access=access_token, refresh=refresh_token)


@auth_bp.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    jwt_redis_blocklist.set(jti, "", ex=JWT_ACCESS_EXPIRES)
    history = LoginHistory.query.filter_by(access_token=jti).one_or_none()
    if history and history.refresh_token:
        jwt_redis_blocklist.set(
            str(history.refresh_token), "", ex=JWT_REFRESH_EXPIRES
        )
    return jsonify(msg=ACCESS_TOKEN_REVOKED)


@auth_bp.route('/validate', methods=['GET'])
@jwt_required()
def validate_user_by_jwt():
    user_schema = UserSchema()
    return user_schema.dump(current_user)
