"""add title row to posts table

Revision ID: 53d178737e6e
Revises: bd23cdaac516
Create Date: 2021-09-15 16:00:31.433976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53d178737e6e'
down_revision = 'bd23cdaac516'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
    sa.Column('title', sa.String))


def downgrade():
    op.drop_column('posts','title')
