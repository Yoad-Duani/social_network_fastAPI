"""add content to post table

Revision ID: 633e58034f9c
Revises: 53eb847840c6
Create Date: 2021-11-08 09:36:55.659908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '633e58034f9c'
down_revision = '53eb847840c6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
