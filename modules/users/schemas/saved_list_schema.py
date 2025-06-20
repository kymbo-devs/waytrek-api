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

class SaveActivityRequest(BaseModel):
    activity_id: int

class SavedList(BaseModel):
    id: int
    user_id: int
    activity_id: int
    created_at: datetime

class SavedListWithActivity(SavedList):
    activity: SavedListActivity