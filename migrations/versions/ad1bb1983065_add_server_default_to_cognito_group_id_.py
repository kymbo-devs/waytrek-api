"""Add server default to cognito_group_id in users table

Revision ID: ad1bb1983065
Revises: 451b9c89e44d
Create Date: 2025-07-01 11:12:49.467486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad1bb1983065'
down_revision: Union[str, None] = '451b9c89e44d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        BEGIN;
        ALTER TABLE users ADD COLUMN cognito_group_id VARCHAR NOT NULL DEFAULT 'GENERAL_USER';
        COMMIT;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        BEGIN;
        ALTER TABLE users DROP COLUMN cognito_group_id;
        COMMIT;
    """)
