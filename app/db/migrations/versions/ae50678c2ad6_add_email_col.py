"""Add email col

Revision ID: ae50678c2ad6
Revises: 75c80cff56bd
Create Date: 2021-06-14 10:54:33.452214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae50678c2ad6'
down_revision = '75c80cff56bd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'users', sa.Column('email', sa.String(length=128), nullable=False)
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###