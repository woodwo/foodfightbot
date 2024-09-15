"""update attack power to calories

Revision ID: 1fee42e0bcdf
Revises: ff09a4c92707
Create Date: 2024-04-11 13:00:32.167961

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1fee42e0bcdf"
down_revision: Union[str, None] = "ff09a4c92707"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # write the SQL statement to update the data
    sql_statements = [
        "UPDATE fighters SET attack_power = 1280 WHERE name = 'Dumpling';",
        "UPDATE fighters SET attack_power = 2000 WHERE name = 'Kebab';",
        "UPDATE fighters SET attack_power = 420 WHERE name = 'Nuggets';",
        "UPDATE fighters SET attack_power = 1200 WHERE name = 'Pizza';",
        "UPDATE fighters SET attack_power = 540 WHERE name = 'Toblerone';",
        "UPDATE fighters SET attack_power = 800 WHERE name = 'Ramen';",
    ]

    for sql in sql_statements:
        op.execute(sa.text(sql))


def downgrade() -> None:
    pass
