"""roles Column add

Revision ID: 2d5e154c58a1
Revises: 
Create Date: 2025-10-05 04:20:24.729243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d5e154c58a1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users",sa.Column("roles" ,sa.String(20),server_default="regular"))
    pass


def downgrade() -> None:
    op.drop_column("users","roles")
    pass
