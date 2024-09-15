"""new fighters

Revision ID: e7a6c7f91a6c
Revises: 1fee42e0bcdf
Create Date: 2024-04-16 17:33:31.714605

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e7a6c7f91a6c"
down_revision: Union[str, None] = "1fee42e0bcdf"
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
    """
    Bento [🍱] Attack power: 525 calories
    Onigiri [🍙] Attack power: 100-150 calories
    French fries [🍟] Attack power: 312 calories
    Burger [🍔] Attack power: 354 calories
    Hotdog [🌭] Attack power: 290 calories
    Pancakes [🥞] Attack power: 700 calories
    """

    # define the data to insert
    data = [
        {
            "name": "Bento",
            "icon": "🍱",
            "attack_power": 525,
            "description": "Bento, a sushi-armored warrior, wields chopsticks as his weapon, defending the honor of lunchboxes with tofu shields in hand. Ready to battle, he charges into the fray against his food foes.",
        },
        {
            "name": "Onigiri",
            "icon": "🍙",
            "attack_power": 150,
            "description": "Onigiri is a stoic warrior, silent and focused. It exudes an aura of quiet power. It's a triangular behemoth, meticulously shaped and formed from the strongest, stickiest rice. A thick band of toasted seaweed (nori) wraps its base, forming a sturdy belt.",
        },
        {
            "name": "French fries",
            "icon": "🍟",
            "attack_power": 312,
            "description": "The Fry Legion is a battalion of seasoned soldiers, each fry a golden warrior, standing tall and united.",
        },
        {
            "name": "Burger",
            "icon": "🍔",
            "attack_power": 354,
            "description": "Burger believes himself to be the rightful ruler of all food fights, a champion of flavor and culinary dominance.",
        },
        {
            "name": "Hotdog",
            "icon": "🌭",
            "attack_power": 290,
            "description": "The hottest one's always a winner!",
        },
        {
            "name": "Pancakes",
            "icon": "🥞",
            "attack_power": 700,
            "description": "Hurrrr, the flying pancake, soars through the skies with a buttery cape billowing behind him, leaving a trail of syrupy justice in his wake. They bring their spatula too.",
        },
    ]

    # insert the data
    op.bulk_insert(fighters, data)


def downgrade() -> None:
    pass
