"""create user table

Revision ID: d460b5194400
Revises: 
Create Date: 2020-11-06 14:42:52.221751-05:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd460b5194400'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("user",
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("email", sa.String(50), nullable=False),
                    sa.Column("first_name", sa.String(50)),
                    sa.Column("last_name", sa.String(50)),
                    sa.Column("location", sa.String(50)),
                    sa.Column("hashed_password", sa.String(100), nullable=False),
                    sa.Column("is_active", sa.Boolean, nullable=False))


def downgrade():
    op.drop_table("user")
