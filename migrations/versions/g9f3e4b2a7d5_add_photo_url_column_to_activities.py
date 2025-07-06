"""add_photo_url_column_to_activities

Revision ID: g9f3e4b2a7d5
Revises: f8e2d3a1b9c6
Create Date: 2025-07-05 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'g9f3e4b2a7d5'
down_revision: Union[str, None] = 'f8e2d3a1b9c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        BEGIN;
        -- Running upgrade f8e2d3a1b9c6 -> g9f3e4b2a7d5
        ALTER TABLE activities
        ADD COLUMN photo_url VARCHAR DEFAULT NULL;
        COMMIT;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        BEGIN;
        -- Running downgrade g9f3e4b2a7d5 -> f8e2d3a1b9c6
        ALTER TABLE activities
        DROP COLUMN photo_url;
        COMMIT;
    """)
