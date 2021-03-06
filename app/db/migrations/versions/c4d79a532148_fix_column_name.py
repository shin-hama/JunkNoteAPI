"""Fix column name

Revision ID: c4d79a532148
Revises: c3c6a40821a1
Create Date: 2021-09-09 00:53:23.063068

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c4d79a532148'
down_revision = 'c3c6a40821a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('memos', sa.Column('removed', sa.Boolean(), nullable=False))
    op.drop_index('ix_memos_is_removed', table_name='memos')
    op.create_index(op.f('ix_memos_removed'), 'memos', ['removed'], unique=False)
    op.drop_column('memos', 'is_removed')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('memos', sa.Column('is_removed', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_memos_removed'), table_name='memos')
    op.create_index('ix_memos_is_removed', 'memos', ['is_removed'], unique=False)
    op.drop_column('memos', 'removed')
    # ### end Alembic commands ###
