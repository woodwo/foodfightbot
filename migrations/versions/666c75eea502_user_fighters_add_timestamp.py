"""User fighters: add timestamp

Revision ID: 666c75eea502
Revises: 4fbd0cb229ee
Create Date: 2024-04-10 21:09:19.368050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '666c75eea502'
down_revision: Union[str, None] = '4fbd0cb229ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # create a new table with the new column
    op.create_table(
        'user_fighters_new',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('fighter_id', sa.Integer, sa.ForeignKey('fighters.id'), primary_key=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # copy data from the old table to the new table
    op.execute('INSERT INTO user_fighters_new (user_id, fighter_id) SELECT user_id, fighter_id FROM user_fighters')

    # drop the old table
    op.drop_table('user_fighters')

    # rename the new table to the old table's name
    op.rename_table('user_fighters_new', 'user_fighters')

def downgrade():
    # create a new table without the new column
    op.create_table(
        'user_fighters_new',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('fighter_id', sa.Integer, sa.ForeignKey('fighters.id'), primary_key=True),
    )

    # copy data from the old table to the new table
    op.execute('INSERT INTO user_fighters_new (user_id, fighter_id) SELECT user_id, fighter_id FROM user_fighters')

    # drop the old table
    op.drop_table('user_fighters')

    # rename the new table to the old table's name
    op.rename_table('user_fighters_new', 'user_fighters')