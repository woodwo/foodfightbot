"""Add initial fighters

Revision ID: da5e0a957139
Revises: fc6e23945c86
Create Date: 2024-04-08 11:01:49.422418

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "da5e0a957139"
down_revision: Union[str, None] = "fc6e23945c86"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # create a reference to the fighters table
    fighters = sa.table(
        "fighters",
        sa.Column("name", sa.String),
        sa.Column("icon", sa.String),
        sa.Column("attack_power", sa.Integer),
        sa.Column("description", sa.String),
    )

    # define the data to insert
    data = [
        {
            "name": "Dumpling",
            "icon": "🥟",
            "attack_power": 19,
            "description": "One dumpling will always turn into two dumplings. Two dumplings will turn into four. Call your dumpling friends to surround the enemy!",
        },
        {
            "name": "Kebab",
            "icon": "🥙",
            "attack_power": 14,
            "description": "Feed your enemies some kebab! Oops, it looks like your kebab was made out of rotten meat! What did you expect from streetfood?",
        },
        {
            "name": "Nuggets",
            "icon": "🍗",
            "attack_power": 22,
            "description": "Nuggets are the best choice for a quick meal. They are also the best choice for a quick fight!",
        },
        {
            "name": "Pizza",
            "icon": "🍕",
            "attack_power": 16,
            "description": "This pizza sure has a lot of cheese! It looks like the enemy can't move... The cheese blocked him! Get your enemy stuck in cheese!",
        },
        {
            "name": "Toblerone",
            "icon": "🍫",
            "attack_power": 13,
            "description": "Mmmm, what a delicious toblerone! The enemy seems distracted, he is busy eating toblerone..! Attack now!",
        },
        {
            "name": "Ramen",
            "icon": "🍜",
            "attack_power": 20,
            "description": "Tie up your enemy with noodles and dip him in broth! This delicious ramen is unfortunately very aggressive",
        },
    ]

    # insert the data
    op.bulk_insert(fighters, data)


def downgrade():
    # create a reference to the fighters table
    fighters = sa.table("fighters", sa.Column("name", sa.String))

    # define the names of the fighters to delete
    names = ["Dumpling", "Kebab", "Nuggets", "Pizza", "Toblerone", "Ramen"]

    # delete the fighters
    for name in names:
        op.execute(fighters.delete().where(fighters.c.name == name))
