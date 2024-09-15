"""add next win to user

Revision ID: ff09a4c92707
Revises: 666c75eea502
Create Date: 2024-04-10 21:50:00.762377

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ff09a4c92707"
down_revision: Union[str, None] = "666c75eea502"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("next_win_count", sa.Integer(), nullable=True, default=3)
    )


def downgrade() -> None:
    op.drop_column("users", "next_win_count")
