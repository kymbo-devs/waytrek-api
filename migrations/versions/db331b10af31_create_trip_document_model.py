"""create trip document model

Revision ID: db331b10af31
Revises: 6fdfaa630eb9
Create Date: 2025-06-05 18:24:50.767711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db331b10af31'
down_revision: Union[str, None] = '6fdfaa630eb9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        BEGIN;
        -- Running upgrade 6fdfaa630eb9 -> db331b10af31
        CREATE TABLE trip_documents (
            id SERIAL NOT NULL, 
            trip_id INTEGER, 
            url VARCHAR NOT NULL, 
            type VARCHAR NOT NULL, 
            file_key VARCHAR NOT NULL, 
            PRIMARY KEY (id), 
            FOREIGN KEY(trip_id) REFERENCES trips (id) ON DELETE cascade
        );
        COMMIT;
    """)


def downgrade() -> None:
    op.execute("""
        BEGIN;
        -- Running downgrade db331b10af31 -> 6fdfaa630eb9
        DROP TABLE trip_documents;
        COMMIT;
    """)
