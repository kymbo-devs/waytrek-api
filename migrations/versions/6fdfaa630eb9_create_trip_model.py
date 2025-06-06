"""create trip model

Revision ID: 6fdfaa630eb9
Revises: caeb0c765198
Create Date: 2025-06-05 18:24:41.675283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fdfaa630eb9'
down_revision: Union[str, None] = 'caeb0c765198'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        BEGIN;
        -- Running upgrade caeb0c765198 -> 6fdfaa630eb9
        CREATE TABLE trips (
            id SERIAL NOT NULL, 
            user_id INTEGER, 
            location_id INTEGER, 
            PRIMARY KEY (id), 
            FOREIGN KEY(location_id) REFERENCES locations (id) ON DELETE cascade, 
            FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE cascade
        );
        COMMIT;
    """)


def downgrade() -> None:
    op.execute("""
        BEGIN;
        -- Running downgrade 6fdfaa630eb9 -> caeb0c765198
        DROP TABLE trips;
        COMMIT;
    """)
