"""new fighters again

Revision ID: cf1a62d802cb
Revises: e7a6c7f91a6c
Create Date: 2024-09-15 12:24:02.178702

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cf1a62d802cb"
down_revision: Union[str, None] = "e7a6c7f91a6c"
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
    Finn crisp [🍞] Attack power: 20 calories
    Ice cream cone [🍦] Attack power: 280 calories
    Mochi [🍡] Attack power: 310 calories

    Sandwich [🥪] Attack power: 330 calories
    Pretzel [🥨] Attack power: 380 calories
    Cupcake [🧁] Attack power: 305 calories
    """

    # define the data to insert
    data = [
        {
            "name": "Finn crisp",
            "icon": "🍞",
            "attack_power": 20,
            "description": "It dries you out and cuts your mouth! This durable crisp can beat any enemy with it's sharp corners.",
        },
        {
            "name": "Ice cream cone",
            "icon": "🍦",
            "attack_power": 280,
            "description": "This cold creamy warrior will give you a brain freeze. Don't try to stab him as he is protected with high-quality waffle armor.",
        },
        {
            "name": "Mochi",
            "icon": "🍡",
            "attack_power": 310,
            "description": "It will get stuck in it's enemy's throat, choking him to death. Soft in the inside, but stretchy and chewy on the outside. Fear the great mochi!",
        },
        {
            "name": "Sandwich",
            "icon": "🥪",
            "attack_power": 330,
            "description": "He's not as simple as it seems. He is a skilled warrior, especially good at fighting hunger - you all experienced it's power.",
        },
        {
            "name": "Pretzel",
            "icon": "🥨",
            "attack_power": 380,
            "description": "This salty creature will make you thirsty and weak. It's twisted shape is a symbol of it's twisted mind.",
        },
        {
            "name": "Cupcake",
            "icon": "🧁",
            "attack_power": 305,
            "description": "Hidden under a soft hat of icing there is a true beast, a bomb full of carbs that send your blood sugar level to a roller coaster",
        },
    ]

    # insert the data
    op.bulk_insert(fighters, data)


def downgrade() -> None:
    pass
