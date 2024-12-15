"""add_notifications_enabled

Revision ID: bebfe7b62101
Revises: cf1a62d802cb
Create Date: 2024-12-15 14:17:51.045240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bebfe7b62101'
down_revision: Union[str, None] = 'cf1a62d802cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', 
        sa.Column('notifications_enabled', sa.Boolean(), 
        server_default='false', nullable=False))

def downgrade() -> None:
    op.drop_column('users', 'notifications_enabled')
