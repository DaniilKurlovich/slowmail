"""add column with delay letter

Revision ID: 6333dc7ec84b
Revises: 930a688d0ca2
Create Date: 2020-11-12 14:54:37.347537-05:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6333dc7ec84b'
down_revision = '930a688d0ca2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('coming_message',
                  sa.Column('delay', sa.Integer, nullable=False)
                  )


def downgrade():
    raise NotImplementedError()
