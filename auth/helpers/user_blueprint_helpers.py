from http.client import BAD_REQUEST, CONFLICT, NOT_FOUND, FORBIDDEN
from typing import Tuple, Dict, Optional
from uuid import UUID

from helpers.messages import (
    NOT_FOUND_MESSAGE,
    EMAIL_TAKEN_MESSAGE,
    EMAIL_REQUIRED_MESSAGE,
    INVALID_PASSWORD_MESSAGE,
    ADMIN_PERMISSIONS_REQUIRED,
)
from models import User, Roles

RESPONSE_MESSAGE_TEMPLATE = {'msg': ''}


def find_user_by_id(uuid: UUID) -> Optional[User]:
    user = User.query.filter_by(id=uuid).first()
    return user


def error_404_on_no_user(user: Optional[User]) -> Optional[Tuple[Dict, int]]:
    data = RESPONSE_MESSAGE_TEMPLATE.copy()
    if not user:
        data['msg'] = NOT_FOUND_MESSAGE
        return data, NOT_FOUND


def error_400_on_empty_email(email: str) -> Optional[Tuple[Dict, int]]:
    data = RESPONSE_MESSAGE_TEMPLATE.copy()
    if not email:
        data['msg'] = EMAIL_REQUIRED_MESSAGE
        return data, BAD_REQUEST


def error_409_on_email_already_taken(email: str) -> Optional[Tuple[Dict, int]]:
    data = RESPONSE_MESSAGE_TEMPLATE.copy()
    if User.query.filter_by(email=email).first():
        data['msg'] = EMAIL_TAKEN_MESSAGE
        return data, CONFLICT


def error_403_on_admin_role_changing_by_not_admin(
    changing_user: User, requested_role: Roles
) -> Optional[Tuple[Dict, int]]:
    data = RESPONSE_MESSAGE_TEMPLATE.copy()
    if requested_role is Roles.admin and changing_user.role is not Roles.admin:
        data['msg'] = ADMIN_PERMISSIONS_REQUIRED
        return data, FORBIDDEN


def error_403_on_action_on_other_user_by_not_admin(
    user: User, action_performed_user_id: UUID
) -> Optional[Tuple[Dict, int]]:
    data = RESPONSE_MESSAGE_TEMPLATE.copy()
    if user.role is not Roles.admin and action_performed_user_id != user.id:
        data['msg'] = ADMIN_PERMISSIONS_REQUIRED
        return data, FORBIDDEN


def create_new_user(
    email: str,
    password: str,
    first_name: Optional[str],
    last_name: Optional[str],
    role: Roles,
) -> User:
    user = User(
        email=email,
        password=password,
        first_name='',
        last_name='',
        role=Roles.user,
    )
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if role and role is not Roles.user:
        user.role = role
    return user


def error_400_on_password_mismatch(
    user: User, password: str
) -> Optional[Tuple[Dict, int]]:
    data = RESPONSE_MESSAGE_TEMPLATE.copy()
    if not user.check_password(password):
        data['msg'] = INVALID_PASSWORD_MESSAGE
        return data, BAD_REQUEST
