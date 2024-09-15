"""Fighter defaults: data

Revision ID: fabcf25c4321
Revises: bcd1a155e417
Create Date: 2024-04-08 14:58:25.299012

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import update
from sqlalchemy import table, column, String, Boolean


# revision identifiers, used by Alembic.
revision: str = "fabcf25c4321"
down_revision: Union[str, None] = "bcd1a155e417"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    fighters = table("fighters", column("name", String), column("is_default", Boolean))

    op.execute(
        update(fighters)
        .where(fighters.c.name.in_(["Dumpling", "Kebab", "Nuggets"]))
        .values(is_default=True)
    )


def downgrade() -> None:
    fighters = table("fighters", column("name", String), column("is_default", Boolean))

    op.execute(
        update(fighters)
        .where(fighters.c.name.in_(["Dumpling", "Kebab", "Nuggets"]))
        .values(is_default=False)
    )
