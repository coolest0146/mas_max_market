"""add quantity to order

Revision ID: 95a039e2e70b
Revises: 2d5e154c58a1
Create Date: 2025-10-05 05:21:58.656203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95a039e2e70b'
down_revision: Union[str, Sequence[str], None] = '2d5e154c58a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("Orders",sa.Column("quantity" ,sa.Integer))
    op.add_column("Orders",sa.Column("Status" ,sa.String(50),server_default="unconfirmed"))
    pass


def downgrade() -> None:
    op.drop_column("Orders","quantity")
    pass
