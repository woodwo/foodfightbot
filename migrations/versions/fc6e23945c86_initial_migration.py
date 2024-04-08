"""Initial migration

Revision ID: fc6e23945c86
Revises: 
Create Date: 2024-04-08 10:58:55.436087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc6e23945c86'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'fighters',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('icon', sa.String, nullable=False),
        sa.Column('attack_power', sa.Integer, nullable=False),
        sa.Column('description', sa.String, nullable=False),
    )

def downgrade():
    op.drop_table('fighters')
    
