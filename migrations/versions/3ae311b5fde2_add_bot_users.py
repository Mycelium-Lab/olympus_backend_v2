"""add bot users

Revision ID: 3ae311b5fde2
Revises: 223152812b5f
Create Date: 2021-11-25 22:48:59.949408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ae311b5fde2'
down_revision = '223152812b5f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('bot_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.BigInteger(), nullable=True),
    sa.Column('notifications', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bot_users_chat_id'), 'bot_users', ['chat_id'], unique=True)


def downgrade():
    p.drop_index(op.f('ix_bot_users_chat_id'), table_name='bot_users')
    op.drop_table('bot_users')
