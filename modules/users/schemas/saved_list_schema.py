from datetime import datetime
from pydantic import BaseModel

class SavedListActivity(BaseModel):
    id: int
    name: str
    description: str
    location_id: int
    is_active: bool
    history: str
    tip: str
    movie: str
    clothes: str

class SavedListWithActivity(BaseModel):
    id: int
    user_id: int
    activity_id: int
    created_at: datetime
    activity: SavedListActivity