"""create trip schedule model

Revision ID: 8435193ed71c
Revises: db331b10af31
Create Date: 2025-06-05 18:25:21.612174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8435193ed71c'
down_revision: Union[str, None] = 'db331b10af31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        BEGIN;
        -- Running upgrade db331b10af31 -> 8435193ed71c
        CREATE TABLE trip_schedule (
            id SERIAL NOT NULL, 
            trip_id INTEGER, 
            date TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
            PRIMARY KEY (id), 
            FOREIGN KEY(trip_id) REFERENCES trips (id) ON DELETE cascade
        );
        COMMIT;    
    """)


def downgrade() -> None:
    op.execute("""
        BEGIN;
        -- Running downgrade 8435193ed71c -> db331b10af31
        DROP TABLE trip_schedule;
        COMMIT;
    """)
