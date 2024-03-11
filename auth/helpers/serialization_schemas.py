from marshmallow_enum import EnumField

from models import User, LoginHistory, Roles
from settings.extensions import ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    id = ma.auto_field()
    email = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    last_login = ma.auto_field()
    role = EnumField(Roles, by_value=True)


class UserLoginHistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LoginHistory

    date = ma.auto_field()
    user_agent = ma.auto_field()
    user_device_type = ma.auto_field()
