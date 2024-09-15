"""rename winner to fighter

Revision ID: 60cd24958681
Revises: 74e743cbdabb
Create Date: 2024-04-10 20:29:17.626261

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "60cd24958681"
down_revision: Union[str, None] = "74e743cbdabb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column("fight_results", "winner", new_column_name="fighter")


def downgrade():
    op.alter_column("fight_results", "fighter", new_column_name="winner")
