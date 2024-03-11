import datetime
import enum
import uuid

from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

from settings.extensions import db


class Roles(enum.Enum):
    user = 'user'
    privileged_user = 'privileged_user'
    admin = 'admin'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean(True))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    role = db.Column(
        db.Enum(Roles, name='user_roles'), default=Roles.user, nullable=False
    )
    history = db.relationship(
        'LoginHistory',
        uselist=True,
        back_populates='user',
        passive_deletes=True,
    )

    db.Index('idx_user_email_password', 'email', 'password')

    def __init__(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        role: Roles,
    ) -> None:
        self.email = email
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.is_active = True

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f'<id {self.id}>'


class LoginHistory(db.Model):
    __tablename__ = 'logins_history'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_agent = db.Column(db.String(), nullable=False)
    user_device_type = db.Column(db.String(100), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    access_token = db.Column(UUID(as_uuid=True), nullable=True)
    refresh_token = db.Column(UUID(as_uuid=True), nullable=True)

    user = db.relationship('User', uselist=False, back_populates='history')

    def __init__(
        self,
        user_agent: str,
        user_device_type: str,
        access_token: str,
        refresh_token: str,
    ) -> None:
        self.user_agent = user_agent
        self.user_device_type = user_device_type
        self.access_token = access_token
        self.refresh_token = refresh_token

    def __repr__(self) -> str:
        return f'<id {self.id}>'

