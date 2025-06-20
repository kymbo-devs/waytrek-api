"""add_tags_to_activities

Revision ID: 1727504cfe2c
Revises: 2a1abcdb7166
Create Date: 2025-06-19 23:22:17.504662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '1727504cfe2c'
down_revision: Union[str, None] = '2a1abcdb7166'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        BEGIN;
        -- Running upgrade 2a1abcdb7166 -> 1727504cfe2c
        ALTER TABLE activities
        ADD COLUMN tags TEXT[] DEFAULT '{}';
        COMMIT;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        BEGIN;
        -- Running downgrade 1727504cfe2c -> 2a1abcdb7166
        ALTER TABLE activities
        DROP COLUMN tags;
        COMMIT;
    """)
