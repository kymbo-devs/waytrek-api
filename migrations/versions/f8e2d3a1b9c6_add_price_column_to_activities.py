"""add_price_column_to_activities

Revision ID: f8e2d3a1b9c6
Revises: ad1bb1983065
Create Date: 2025-07-05 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'f8e2d3a1b9c6'
down_revision: Union[str, None] = 'ad1bb1983065'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        BEGIN;
        -- Running upgrade ad1bb1983065 -> f8e2d3a1b9c6
        ALTER TABLE activities
        ADD COLUMN price DECIMAL(10,2) DEFAULT NULL;
        COMMIT;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        BEGIN;
        -- Running downgrade f8e2d3a1b9c6 -> ad1bb1983065
        ALTER TABLE activities
        DROP COLUMN price;
        COMMIT;
    """)
