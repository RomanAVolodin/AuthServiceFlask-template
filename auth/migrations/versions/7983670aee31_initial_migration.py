"""Initial migration.

Revision ID: 7983670aee31
Revises: 
Create Date: 2024-03-11 21:18:24.237153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7983670aee31'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(create_constraint=True), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('role', sa.Enum('user', 'privileged_user', 'admin', name='user_roles'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email'))
    )
    op.create_table('logins_history',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('user_agent', sa.String(), nullable=False),
    sa.Column('user_device_type', sa.String(length=100), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('access_token', sa.UUID(), nullable=True),
    sa.Column('refresh_token', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_logins_history_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_logins_history'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('logins_history')
    op.drop_table('users')
    # ### end Alembic commands ###