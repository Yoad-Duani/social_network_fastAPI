"""create posts table

Revision ID: 53eb847840c6
Revises: 
Create Date: 2021-11-08 09:22:31.255966

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = '53eb847840c6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
        primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
