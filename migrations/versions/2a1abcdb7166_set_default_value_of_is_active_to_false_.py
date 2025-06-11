"""Set default value of is_active to false in Activity model

Revision ID: 2a1abcdb7166
Revises: 5cc48b4adff3
Create Date: 2025-06-11 11:21:27.248526

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2a1abcdb7166'
down_revision: Union[str, None] = '5cc48b4adff3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Set default for future inserts and update existing rows
    op.execute("ALTER TABLE activities ALTER COLUMN is_active SET DEFAULT false;")
    op.execute("UPDATE activities SET is_active = false WHERE is_active IS NULL;")
    
    # Enforce the column to be not null
    op.execute("ALTER TABLE activities ALTER COLUMN is_active SET NOT NULL;")


def downgrade() -> None:
    """Downgrade schema."""
    # Revert to nullable and remove the default
    op.execute("ALTER TABLE activities ALTER COLUMN is_active DROP NOT NULL;")
    op.execute("ALTER TABLE activities ALTER COLUMN is_active DROP DEFAULT;")
