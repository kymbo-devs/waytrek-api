"""create user model

Revision ID: bd7347c77341
Revises: 
Create Date: 2025-06-05 18:15:28.087475

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd7347c77341'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        BEGIN;

        CREATE TABLE users (
            id SERIAL NOT NULL,
            name VARCHAR NOT NULL,
            email VARCHAR NOT NULL,
            cognito_id VARCHAR NOT NULL,
            cognito_group_id VARCHAR NOT NULL,
            is_active BOOLEAN,
            PRIMARY KEY (id),
            UNIQUE (cognito_id),
            UNIQUE (email)
        );

        COMMIT;
    """)


def downgrade() -> None:
    op.execute("""
    BEGIN;
    DROP TABLE users;
    COMMIT;    
    """)
    
