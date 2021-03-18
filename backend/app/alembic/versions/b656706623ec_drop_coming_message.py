"""drop coming message

Revision ID: b656706623ec
Revises: 1079179cba9f
Create Date: 2021-02-17 14:39:10.781388-05:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b656706623ec'
down_revision = '1079179cba9f'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('coming_message')


def downgrade():
    pass
