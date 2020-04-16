"""empty message

Revision ID: b5d451a31f64
Revises: 8bd0c565b986
Create Date: 2020-04-16 22:57:43.732598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5d451a31f64'
down_revision = '8bd0c565b986'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_name', table_name='user')
    op.create_index(op.f('ix_user_name'), 'user', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_name'), table_name='user')
    op.create_index('ix_user_name', 'user', ['name'], unique=True)
    # ### end Alembic commands ###
