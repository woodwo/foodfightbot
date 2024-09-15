"""Fight results fighters ids

Revision ID: 4fbd0cb229ee
Revises: 60cd24958681
Create Date: 2024-04-10 20:33:20.957670

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4fbd0cb229ee"
down_revision: Union[str, None] = "60cd24958681"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("fight_results", sa.Column("fighter_id", sa.Integer(), nullable=True))
    op.add_column(
        "fight_results", sa.Column("opponent_id", sa.Integer(), nullable=True)
    )
    with op.batch_alter_table("fight_results") as batch_op:
        batch_op.create_foreign_key(
            "fk_fight_results_fighter", "fighters", ["fighter_id"], ["id"]
        )
        batch_op.create_foreign_key(
            "fk_fight_results_opponent", "fighters", ["opponent_id"], ["id"]
        )
        batch_op.drop_column("fighter")
        batch_op.drop_column("opponent")


def downgrade() -> None:
    op.add_column("fight_results", sa.Column("opponent", sa.VARCHAR(), nullable=False))
    op.add_column("fight_results", sa.Column("fighter", sa.VARCHAR(), nullable=False))
    with op.batch_alter_table("fight_results") as batch_op:
        batch_op.drop_constraint("fk_fight_results_fighter", type_="foreignkey")
        batch_op.drop_constraint("fk_fight_results_opponent", type_="foreignkey")
        batch_op.drop_column("opponent_id")
        batch_op.drop_column("fighter_id")
