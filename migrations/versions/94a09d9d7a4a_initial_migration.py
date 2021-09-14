"""initial migration

Revision ID: 94a09d9d7a4a
Revises: 
Create Date: 2021-09-14 15:10:25.079187

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Boolean, DateTime,  ForeignKey
import datetime

# revision identifiers, used by Alembic.
revision = '94a09d9d7a4a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('users')
    op.drop_table('posts')

def downgrade():
    pass
