"""merge two heads

Revision ID: 451b9c89e44d
Revises: 1727504cfe2c, b6e7ccb1443a
Create Date: 2025-07-01 11:06:50.959356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '451b9c89e44d'
down_revision: Union[str, None] = ('1727504cfe2c', 'b6e7ccb1443a')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
