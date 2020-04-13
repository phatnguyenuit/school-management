"""empty message

Revision ID: 190e4e064cf6
Revises: 4745e4940f37
Create Date: 2020-04-12 22:40:53.760018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '190e4e064cf6'
down_revision = '4745e4940f37'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_hash', sa.String(length=128), nullable=True))
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_name'), 'user', ['name'], unique=True)
    op.drop_constraint('user_email_key', 'user', type_='unique')
    op.drop_constraint('user_name_key', 'user', type_='unique')
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.VARCHAR(length=192), autoincrement=False, nullable=True))
    op.create_unique_constraint('user_name_key', 'user', ['name'])
    op.create_unique_constraint('user_email_key', 'user', ['email'])
    op.drop_index(op.f('ix_user_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_column('user', 'password_hash')
    # ### end Alembic commands ###