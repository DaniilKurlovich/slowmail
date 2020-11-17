"""conversation table

Revision ID: 1079179cba9f
Revises: afb03fbe983d
Create Date: 2020-11-15 08:56:07.569932-05:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1079179cba9f'
down_revision = 'afb03fbe983d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('conversation_ids',
                    sa.Column('chat_id', sa.Integer, primary_key=True),
                    sa.Column('from_id', sa.Integer, sa.ForeignKey('user.id'), nullable=False),
                    sa.Column('to_id', sa.Integer, sa.ForeignKey('user.id'), nullable=False))


def downgrade():
    op.drop_table('conversation_ids')
