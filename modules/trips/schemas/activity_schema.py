from typing import NotRequired, Optional
from pydantic import BaseModel
from typing_extensions import TypedDict


class ActivityVideosResponse(TypedDict):
    video_id: int
    title: str
    description: str
    activity_id: int
    file_key: str

class ActivityVideosFilters(BaseModel):
    activity_id: Optional[int] = None