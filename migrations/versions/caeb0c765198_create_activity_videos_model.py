"""create activity videos model

Revision ID: caeb0c765198
Revises: aaabb099fb08
Create Date: 2025-06-05 18:24:30.538833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'caeb0c765198'
down_revision: Union[str, None] = 'aaabb099fb08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        BEGIN;
        -- Running upgrade aaabb099fb08 -> caeb0c765198
        CREATE TABLE activity_videos (
            id SERIAL NOT NULL, 
            activity_id INTEGER, 
            url VARCHAR NOT NULL, 
            file_key VARCHAR NOT NULL, 
            title VARCHAR NOT NULL, 
            description VARCHAR NOT NULL, 
            PRIMARY KEY (id), 
            FOREIGN KEY(activity_id) REFERENCES activities (id) ON DELETE cascade
        );
        COMMIT;    
    """)


def downgrade() -> None:
    op.execute("""
        BEGIN;
        -- Running downgrade aaabb099fb08 -> 430d4aca0df8
        DROP TABLE activity_videos;
        COMMIT;
    """)
