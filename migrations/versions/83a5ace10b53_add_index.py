"""Add index.

Revision ID: 83a5ace10b53
Revises: 086f4a27005a
Create Date: 2020-11-15 06:00:06.044816

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "83a5ace10b53"
down_revision = "086f4a27005a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(
        op.f("ix_ticker_currency_code"), "ticker", ["currency_code"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_ticker_currency_code"), table_name="ticker")
    # ### end Alembic commands ###
