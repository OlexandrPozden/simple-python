"""create tables

Revision ID: bd23cdaac516
Revises: 94a09d9d7a4a
Create Date: 2021-09-14 15:25:55.152794

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Boolean, DateTime,  ForeignKey
import datetime


# revision identifiers, used by Alembic.
revision = 'bd23cdaac516'
down_revision = '94a09d9d7a4a'
branch_labels = None
depends_on = None


def upgrade():
    ## here was  create user table, but I have remove that. Cause, i dont know how, but it works
    ## but alembic created users table but not posts table. so forced to create tables independently
    op.create_table(
        'posts',
        Column('post_id',sa.Integer, primary_key=True, autoincrement=True),
        Column('text',String,nullable=False),
        Column('user_id',Integer, ForeignKey('users.user_id', ondelete="CASCADE")),
        Column('published',Boolean, default=False, nullable=False),
        Column('request_publish',Boolean, default=False, nullable=False),
        Column('published_time', DateTime),
        Column('created_time',DateTime, default=datetime.datetime.now, nullable=False),
        Column('updated_time',DateTime, default=datetime.datetime.now, nullable=False)
    )


def downgrade():
    op.drop_table('posts')
    op.drop_table('users')
