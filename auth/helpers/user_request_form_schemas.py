from marshmallow import Schema, fields, validate

from helpers.messages import (
    EMAIL_REQUIRED_MESSAGE,
    PASSWORD_REQUIRED_MESSAGE,
    NEW_PASSWORD_REQUIRED_MESSAGE,
    ROLE_REQUIRED_MESSAGE,
)
from models import Roles


class CreateUserRequestFormSchema(Schema):
    email = fields.Email(
        required=True, error_messages={'required': EMAIL_REQUIRED_MESSAGE}
    )
    password = fields.Str(
        required=True,
        validate=[validate.Length(min=6, max=36)],
        error_messages={'required': PASSWORD_REQUIRED_MESSAGE},
    )
    first_name = fields.Str()
    last_name = fields.Str()

    # For only admins being able to create admin, for testing please comment
    role = fields.Str(
        validate=[
            validate.OneOf(
                [
                    role.value
                    for role in Roles
                    if role.value != Roles.admin.value
                ]
            )
        ]
    )


class CreateAdminUserRequestFormSchema(Schema):
    email = fields.Email(
        required=True, error_messages={'required': EMAIL_REQUIRED_MESSAGE}
    )
    password = fields.Str(
        required=True,
        validate=[validate.Length(min=6, max=36)],
        error_messages={'required': PASSWORD_REQUIRED_MESSAGE},
    )
    first_name = fields.Str()
    last_name = fields.Str()


class ChangePasswordRequestFormSchema(Schema):
    password = fields.Str(
        required=True,
        validate=[validate.Length(min=6, max=36)],
        error_messages={'required': PASSWORD_REQUIRED_MESSAGE},
    )
    new_password = fields.Str(
        required=True,
        validate=[validate.Length(min=6, max=36)],
        error_messages={'required': NEW_PASSWORD_REQUIRED_MESSAGE},
    )
    new_password_again = fields.Str(
        required=True,
        validate=[validate.Length(min=6, max=36)],
        error_messages={'required': NEW_PASSWORD_REQUIRED_MESSAGE},
    )


class ChangeRoleRequestFormSchema(Schema):
    role = fields.Str(
        required=True,
        validate=[validate.OneOf([role.value for role in Roles])],
        error_messages={'required': ROLE_REQUIRED_MESSAGE},
    )
