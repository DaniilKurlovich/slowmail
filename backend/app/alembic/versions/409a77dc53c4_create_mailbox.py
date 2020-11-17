"""create mailbox

Revision ID: 409a77dc53c4
Revises: d460b5194400
Create Date: 2020-11-12 13:16:10.906212-05:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '409a77dc53c4'
down_revision = 'd460b5194400'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('mailbox',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('to_addr', sa.Integer, sa.ForeignKey('user.id'), nullable=False),
                    sa.Column('from_addr', sa.Integer, sa.ForeignKey('user.id'), nullable=False),
                    sa.Column('received', sa.DateTime, nullable=False),
                    sa.Column('message', sa.String(500), nullable=False))


def downgrade():
    op.create_table('mailbox')