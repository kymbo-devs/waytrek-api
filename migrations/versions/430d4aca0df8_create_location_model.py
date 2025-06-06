"""create location model

Revision ID: 430d4aca0df8
Revises: bc845b156747
Create Date: 2025-06-05 18:21:23.484148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '430d4aca0df8'
down_revision: Union[str, None] = 'bc845b156747'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        BEGIN;
        -- Running upgrade bc845b156747 -> 430d4aca0df8
        CREATE TABLE locations (
            id SERIAL NOT NULL, 
            country VARCHAR NOT NULL, 
            city VARCHAR, 
            nickname VARCHAR, 
            flag_url VARCHAR, 
            PRIMARY KEY (id)
        );
        COMMIT;
    """)


def downgrade() -> None:
    op.execute("""
        BEGIN;
        -- Running downgrade 430d4aca0df8 -> bc845b156747
        DROP TABLE locations;
        COMMIT;
    """)
