from http.client import BAD_REQUEST, CREATED, NO_CONTENT, OK
from uuid import UUID

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user
from werkzeug.security import generate_password_hash

from helpers.serialization_schemas import UserSchema, UserLoginHistorySchema
from helpers.user_blueprint_helpers import (
    find_user_by_id,
    error_404_on_no_user,
    error_409_on_email_already_taken,
    create_new_user,
    error_400_on_empty_email,
    error_400_on_password_mismatch,
    error_403_on_admin_role_changing_by_not_admin,
    error_403_on_action_on_other_user_by_not_admin,
)
from helpers.user_request_form_schemas import (
    ChangePasswordRequestFormSchema,
    ChangeRoleRequestFormSchema,
    CreateAdminUserRequestFormSchema,
    CreateUserRequestFormSchema,
)
from models import Roles, User
from settings.extensions import db

user_bp = Blueprint('user', __name__)


@user_bp.route('', methods=['POST'])
def add_user():
    form_schema = CreateUserRequestFormSchema()
    errors = form_schema.validate(request.json)
    if errors:
        return errors, BAD_REQUEST

    email = request.json.get('email')
    password = request.json.get('password')
    first_name = request.json.get('first_name', None)
    last_name = request.json.get('last_name', None)
    role = request.json.get('role', None)

    error_409 = error_409_on_email_already_taken(email)
    if error_409:
        return error_409

    new_user = create_new_user(email, password, first_name, last_name, role)
    db.session.add(new_user)
    db.session.commit()

    user = User.query.filter_by(email=email).first()
    return '', CREATED


@user_bp.route('/admin', methods=['POST'])
@jwt_required()
def add_admin():
    error_403 = error_403_on_admin_role_changing_by_not_admin(
        current_user, Roles.admin
    )
    if error_403:
        return error_403

    form_schema = CreateAdminUserRequestFormSchema()
    errors = form_schema.validate(request.json)
    if errors:
        return errors, BAD_REQUEST

    email = request.json.get('email')
    password = request.json.get('password')
    first_name = request.json.get('first_name', None)
    last_name = request.json.get('last_name', None)

    error_409 = error_409_on_email_already_taken(email)
    if error_409:
        return error_409

    new_user = create_new_user(
        email, password, first_name, last_name, Roles.admin
    )
    db.session.add(new_user)
    db.session.commit()
    return '', CREATED


@user_bp.route('/<uuid:id>', methods=['GET'])
@jwt_required()
def get_users_details(id: UUID):
    user = find_user_by_id(id)
    error_404 = error_404_on_no_user(user)
    if error_404:
        return error_404
    user_schema = UserSchema()
    return user_schema.dump(user)


@user_bp.route('/<uuid:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id: UUID):
    error_403 = error_403_on_action_on_other_user_by_not_admin(
        current_user, id
    )
    if error_403:
        return error_403

    user = find_user_by_id(id)
    error_404 = error_404_on_no_user(user)
    if error_404:
        return error_404
    user.is_active = False
    db.session.commit()
    return '', NO_CONTENT


@user_bp.route('/<uuid:id>/password', methods=['PATCH'])
@jwt_required()
def change_password(id: UUID):
    error_403 = error_403_on_action_on_other_user_by_not_admin(
        current_user, id
    )
    if error_403:
        return error_403

    form_schema = ChangePasswordRequestFormSchema()
    errors = form_schema.validate(request.json)
    if errors:
        return errors, BAD_REQUEST

    user = find_user_by_id(id)
    error_404 = error_404_on_no_user(user)
    if error_404:
        return error_404

    password = request.json.get('password')
    new_password = request.json.get('new_password')

    error_invalid_password = error_400_on_password_mismatch(user, password)
    if error_invalid_password:
        return error_invalid_password

    user.password = generate_password_hash(new_password)
    db.session.commit()
    return '', OK


@user_bp.route('/<uuid:id>/email', methods=['PATCH'])
@jwt_required()
def change_email(id: UUID):
    error_403 = error_403_on_action_on_other_user_by_not_admin(
        current_user, id
    )
    if error_403:
        return error_403

    email = request.json.get('email', None)

    error_400 = error_400_on_empty_email(email)
    if error_400:
        return error_400

    user = find_user_by_id(id)
    error_404 = error_404_on_no_user(user)
    if error_404:
        return error_404

    user.email = email
    db.session.commit()
    return '', OK


@user_bp.route('/<uuid:id>/role', methods=['PATCH'])
@jwt_required()
def change_role(id: UUID):
    form_schema = ChangeRoleRequestFormSchema()
    errors = form_schema.validate(request.json)
    if errors:
        return errors, BAD_REQUEST

    role = Roles(request.json.get('role'))

    error_403 = error_403_on_admin_role_changing_by_not_admin(
        current_user, role
    )
    if error_403:
        return error_403

    user = find_user_by_id(id)
    error_404 = error_404_on_no_user(user)
    if error_404:
        return error_404

    user.role = role
    db.session.commit()
    return '', OK


@user_bp.route('/<uuid:id>/history', methods=['GET'])
@jwt_required()
def show_users_history(id: UUID):
    error_403 = error_403_on_action_on_other_user_by_not_admin(
        current_user, id
    )
    if error_403:
        return error_403

    user = find_user_by_id(id)
    error_404 = error_404_on_no_user(user)
    if error_404:
        return error_404

    user_logins = user.history
    login_history_schema = UserLoginHistorySchema(many=True)
    return {'data': login_history_schema.dump(user_logins)}
