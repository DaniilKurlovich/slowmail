"""create message queue

Revision ID: 930a688d0ca2
Revises: 409a77dc53c4
Create Date: 2020-11-12 13:16:21.580552-05:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '930a688d0ca2'
down_revision = '409a77dc53c4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('coming_message',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('from_addr', sa.Integer, sa.ForeignKey('user.id'), nullable=False),
                    sa.Column('to_addr', sa.Integer, sa.ForeignKey('user.id'), nullable=False),
                    sa.Column('date', sa.DateTime, nullable=False),
                    sa.Column('message', sa.String(500), nullable=False))


def downgrade():
    op.drop_table('coming_message')
