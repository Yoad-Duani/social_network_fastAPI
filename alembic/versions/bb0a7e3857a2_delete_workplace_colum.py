"""delete workplace colum

Revision ID: bb0a7e3857a2
Revises: e3f596978030
Create Date: 2021-11-09 15:52:19.330209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb0a7e3857a2'
down_revision = 'e3f596978030'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('workPlaces')
    op.add_column('users', sa.Column('company_name', sa.String(), server_default='No Company', nullable=False))
    op.add_column('users', sa.Column('description', sa.String(), server_default='No Description', nullable=False))
    op.add_column('users', sa.Column('position', sa.String(), server_default='No Position', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'position')
    op.drop_column('users', 'description')
    op.drop_column('users', 'company_name')
    op.create_table('workPlaces',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('company_name', sa.VARCHAR(), server_default=sa.text("'No Company'::character varying"), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), server_default=sa.text("'No Description'::character varying"), autoincrement=False, nullable=False),
    sa.Column('position', sa.VARCHAR(), server_default=sa.text("'No Position'::character varying"), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='workPlaces_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', name='workPlaces_pkey')
    )
    # ### end Alembic commands ###
