"""add mark_flag to mailbox

Revision ID: afb03fbe983d
Revises: 6333dc7ec84b
Create Date: 2020-11-14 15:29:00.221551-05:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afb03fbe983d'
down_revision = '6333dc7ec84b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('mailbox',
                  sa.Column('as_read', sa.Boolean, nullable=False)
                  )


def downgrade():
    raise NotImplementedError()
