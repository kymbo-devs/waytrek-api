"""add_population_column_to_activities

Revision ID: h1a4f5c8b9e2
Revises: g9f3e4b2a7d5
Create Date: 2025-07-05 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'h1a4f5c8b9e2'
down_revision: Union[str, None] = 'g9f3e4b2a7d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        BEGIN;
        -- Running upgrade g9f3e4b2a7d5 -> h1a4f5c8b9e2
        ALTER TABLE activities
        ADD COLUMN population INTEGER DEFAULT NULL;
        COMMIT;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        BEGIN;
        -- Running downgrade h1a4f5c8b9e2 -> g9f3e4b2a7d5
        ALTER TABLE activities
        DROP COLUMN population;
        COMMIT;
    """)
