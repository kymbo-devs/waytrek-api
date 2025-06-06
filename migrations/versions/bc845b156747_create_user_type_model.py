"""create user type model

Revision ID: bc845b156747
Revises: bd7347c77341
Create Date: 2025-06-05 18:17:40.721709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc845b156747'
down_revision: Union[str, None] = 'bd7347c77341'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.execute("""
        BEGIN;
        -- Running upgrade bd7347c77341 -> bc845b156747
        CREATE TABLE users_types (
            id SERIAL NOT NULL, 
            name VARCHAR NOT NULL, 
            description VARCHAR NOT NULL, 
            PRIMARY KEY (id)
        );
        ALTER TABLE users ADD COLUMN user_type_id INTEGER;
        ALTER TABLE users ADD FOREIGN KEY(user_type_id) REFERENCES users_types (id) ON DELETE cascade;
        COMMIT;    
    """)
    


def downgrade() -> None:
    op.execute("""
        BEGIN;
        -- Running downgrade bc845b156747 -> bd7347c77341
        ALTER TABLE users DROP COLUMN user_type_id;
        DROP TABLE users_types;
        COMMIT;
    """)
    
