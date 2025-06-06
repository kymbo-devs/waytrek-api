"""create schedule model

Revision ID: 5cc48b4adff3
Revises: 8435193ed71c
Create Date: 2025-06-05 18:25:29.115545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5cc48b4adff3'
down_revision: Union[str, None] = '8435193ed71c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        BEGIN;
        -- Running upgrade 8435193ed71c -> 5cc48b4adff3
        CREATE TABLE schedule (
            id SERIAL NOT NULL, 
            trip_schedule_id INTEGER, 
            hour VARCHAR NOT NULL, 
            activity_name VARCHAR NOT NULL, 
            PRIMARY KEY (id), 
            FOREIGN KEY(trip_schedule_id) REFERENCES trip_schedule (id) ON DELETE cascade
        );
        COMMIT;
    """)


def downgrade() -> None:
    op.execute("""
        BEGIN;
        -- Running downgrade 5cc48b4adff3 -> 8435193ed71c
        DROP TABLE schedule;
        COMMIT;    
    """)
