"""create activity model

Revision ID: aaabb099fb08
Revises: 430d4aca0df8
Create Date: 2025-06-05 18:23:51.008781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aaabb099fb08'
down_revision: Union[str, None] = '430d4aca0df8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        BEGIN;
        -- Running upgrade 430d4aca0df8 -> aaabb099fb08
        CREATE TABLE activities (
            id SERIAL NOT NULL, 
            name VARCHAR NOT NULL, 
            description VARCHAR NOT NULL, 
            location_id INTEGER, 
            is_active BOOLEAN, 
            history VARCHAR NOT NULL, 
            tip VARCHAR NOT NULL, 
            movie VARCHAR NOT NULL, 
            clothes VARCHAR NOT NULL, 
            PRIMARY KEY (id), 
            FOREIGN KEY(location_id) REFERENCES locations (id) ON DELETE cascade
        );
        COMMIT;
    """)


def downgrade() -> None:
    op.execute("""
        BEGIN;
        -- Running downgrade aaabb099fb08 -> 430d4aca0df8
        DROP TABLE activities;
        COMMIT;
    """)
