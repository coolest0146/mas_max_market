"""add Satus ot Order

Revision ID: 652b72c5f6be
Revises: 95a039e2e70b
Create Date: 2025-10-06 00:26:05.893565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '652b72c5f6be'
down_revision: Union[str, Sequence[str], None] = '95a039e2e70b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("Orders",sa.Column("Status" ,sa.String(50),server_default="unconfirmed"))
    pass


def downgrade() -> None:
    op.drop("'Orders","Status")
    pass
