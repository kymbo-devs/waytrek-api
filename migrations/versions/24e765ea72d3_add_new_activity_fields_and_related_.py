"""add_new_activity_fields_and_related_tables

Revision ID: 24e765ea72d3
Revises: h1a4f5c8b9e2
Create Date: 2025-07-11 13:09:52.446799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24e765ea72d3'
down_revision: Union[str, None] = 'h1a4f5c8b9e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        BEGIN;
        -- Running upgrade h1a4f5c8b9e2 -> 24e765ea72d3
        
        -- Add new columns to activities table
        ALTER TABLE activities
        ADD COLUMN title TEXT,
        ADD COLUMN category TEXT,
        ADD COLUMN city TEXT,
        ADD COLUMN country_code TEXT,
        ADD COLUMN location_name TEXT,
        ADD COLUMN weather TEXT,
        ADD COLUMN entrance TEXT,
        ADD COLUMN opening_hours TEXT,
        ADD COLUMN rating FLOAT,
        ADD COLUMN foundation_date TEXT,
        ADD COLUMN price_min INTEGER,
        ADD COLUMN price_max INTEGER;

        -- Create activity_photos table
        CREATE TABLE activity_photos (
            id SERIAL PRIMARY KEY,
            activity_id INTEGER NOT NULL REFERENCES activities(id) ON DELETE CASCADE,
            name TEXT NOT NULL,
            url TEXT NOT NULL
        );

        -- Create activity_reviews table
        CREATE TABLE activity_reviews (
            id SERIAL PRIMARY KEY,
            activity_id INTEGER NOT NULL REFERENCES activities(id) ON DELETE CASCADE,
            content TEXT NOT NULL
        );

        -- Create activity_tips table
        CREATE TABLE activity_tips (
            id SERIAL PRIMARY KEY,
            activity_id INTEGER NOT NULL REFERENCES activities(id) ON DELETE CASCADE,
            tip_type TEXT CHECK (tip_type IN ('foodie', 'weather_clothing', 'pro_traveler')) NOT NULL,
            tip TEXT NOT NULL
        );

        -- Remove obsolete columns
        ALTER TABLE activities
        DROP COLUMN tip,
        DROP COLUMN photo_url,
        DROP COLUMN price;
        
        COMMIT;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        BEGIN;
        -- Running downgrade 24e765ea72d3 -> h1a4f5c8b9e2
        
        -- Add back the removed columns
        ALTER TABLE activities
        ADD COLUMN tip VARCHAR NOT NULL DEFAULT '',
        ADD COLUMN photo_url VARCHAR,
        ADD COLUMN price DECIMAL(10, 2);
        
        -- Drop the new tables
        DROP TABLE activity_tips;
        DROP TABLE activity_reviews;
        DROP TABLE activity_photos;
        
        -- Remove the new columns from activities table
        ALTER TABLE activities
        DROP COLUMN title,
        DROP COLUMN category,
        DROP COLUMN city,
        DROP COLUMN country_code,
        DROP COLUMN location_name,
        DROP COLUMN weather,
        DROP COLUMN entrance,
        DROP COLUMN opening_hours,
        DROP COLUMN rating,
        DROP COLUMN foundation_date,
        DROP COLUMN price_min,
        DROP COLUMN price_max;
        
        COMMIT;
    """)
