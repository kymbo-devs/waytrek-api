"""create saved list model

Revision ID: b6e7ccb1443a
Revises: 2a1abcdb7166
Create Date: 2025-06-19 18:35:36.401145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6e7ccb1443a'
down_revision: Union[str, None] = '2a1abcdb7166'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE saved_list (
      id SERIAL PRIMARY KEY NOT NULL,
      user_id INTEGER NOT NULL,
      activity_id INTEGER NOT NULL,
      created_at TIMESTAMP DEFAULT NOW(),
      FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE cascade,
      FOREIGN KEY(activity_id) REFERENCES activities (id) ON DELETE cascade,
      UNIQUE(user_id, activity_id)
    );
    """)


def downgrade() -> None:
    op.execute("""
        DROP TABLE saved_list;
    """)
