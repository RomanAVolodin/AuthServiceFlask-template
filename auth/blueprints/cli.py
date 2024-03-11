import click
from flask import Blueprint

from helpers.user_blueprint_helpers import (
    error_409_on_email_already_taken,
    create_new_user,
)
from models import Roles
from settings.extensions import db

command_bp = Blueprint('command', __name__)


@command_bp.cli.command('create-privileged-user')
@click.argument('email')
def create_privileged(email: str):
    error_409 = error_409_on_email_already_taken(email)
    if error_409:
        return error_409

    new_user = create_new_user(
        email, 'password', '', '', role=Roles.privileged_user
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user


@command_bp.cli.command('create-admin')
@click.argument('email')
def create_privileged(email: str):
    error_409 = error_409_on_email_already_taken(email)
    if error_409:
        return error_409

    new_user = create_new_user(email, 'password', '', '', role=Roles.admin)
    db.session.add(new_user)
    db.session.commit()
    return new_user
