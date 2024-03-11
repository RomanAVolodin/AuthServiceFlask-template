import datetime

from flask import Request
from typing import Optional, Tuple
import uuid

from flask_jwt_extended import (
    decode_token,
    create_access_token,
    create_refresh_token,
)

from helpers.user_blueprint_helpers import create_new_user
from models import User, LoginHistory, Roles
from settings.extensions import db


def generate_tokens_for_user(user: User) -> Tuple[str, str]:
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    return access_token, refresh_token


def add_login_history_for_user(
    request: Request, user: User, access_token: str, refresh_token: str
) -> None:
    user.history.append(
        LoginHistory(
            user_agent=request.headers.get('User-Agent'),
            user_device_type='desktop',
            access_token=decode_token(access_token)['jti'],
            refresh_token=decode_token(refresh_token)['jti'],
        )
    )
    user.last_login = datetime.datetime.now()
    db.session.commit()
