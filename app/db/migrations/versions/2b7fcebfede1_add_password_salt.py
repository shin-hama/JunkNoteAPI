"""Add password salt

Revision ID: 2b7fcebfede1
Revises: 1ae4af70a2f0
Create Date: 2021-06-17 03:32:50.999770

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2b7fcebfede1'
down_revision = '1ae4af70a2f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('salt', sa.Text(), nullable=False))
    op.alter_column('users', 'username',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('users', 'email',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)
    op.alter_column('users', 'hashed_password',
               existing_type=mysql.VARCHAR(length=60),
               nullable=False)
    op.alter_column('users', 'disabled',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'disabled',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True)
    op.alter_column('users', 'hashed_password',
               existing_type=mysql.VARCHAR(length=60),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)
    op.alter_column('users', 'username',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.drop_column('users', 'salt')
    # ### end Alembic commands ###
