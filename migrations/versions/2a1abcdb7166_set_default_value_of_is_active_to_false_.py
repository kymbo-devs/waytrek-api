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
    op.alter_column('activities', 'is_active',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               server_default=sa.text('false'))


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('activities', 'is_active',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               server_default=sa.text('true'))
